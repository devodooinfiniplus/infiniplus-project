/** @odoo-module **/

import { Component, onMounted, onWillUnmount, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class ExpenseQRScanner extends Component {

    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");

        this.videoRef = useRef("video");
        this.canvas = document.createElement("canvas");
        this.ctx = this.canvas.getContext("2d");

        this.stream = null;
        this.scanInterval = null;
        this._scanned = false; //evita múltiplas leituras

        onMounted(() => this.startCamera());
        onWillUnmount(() => this.stopCamera());
    }

    async startCamera() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: { ideal: "environment" } },
                audio: false,
            });

            const video = this.videoRef.el;
            video.srcObject = this.stream;
            await video.play();

            this.startScanning();

        } catch (error) {
            console.error("Erro ao abrir câmara:", error);
            alert("Não foi possível aceder à câmara.");
        }
    }

    startScanning() {
        const video = this.videoRef.el;

        this.scanInterval = setInterval(() => {

            if (this._scanned) {
                return;
            }

            if (video.readyState !== video.HAVE_ENOUGH_DATA) {
                return;
            }

            this.canvas.width = video.videoWidth;
            this.canvas.height = video.videoHeight;

            this.ctx.drawImage(
                video,
                0,
                0,
                this.canvas.width,
                this.canvas.height
            );

            const imageData = this.ctx.getImageData(
                0,
                0,
                this.canvas.width,
                this.canvas.height
            );

            const qr = jsQR(
                imageData.data,
                imageData.width,
                imageData.height
            );

            if (qr && qr.data) {
                this._scanned = true; //bloqueia novas leituras
                this.processQR(qr.data);
            }

        }, 300);
    }

    stopCamera() {
        if (this.scanInterval) {
            clearInterval(this.scanInterval);
            this.scanInterval = null;
        }

        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
    }

    async processQR(qrString) {

        try {
            this.stopCamera();

            const expenseId = this.props.action?.params?.expense_id;

            if (!expenseId) {
                console.error("Expense ID não encontrado.");
                return;
            }

            await this.orm.write("hr.expense", [expenseId], {
                qr_raw_string: qrString,
            });

            await this.actionService.doAction({
                type: "ir.actions.act_window_close",
            });

        } catch (error) {
            console.error("Erro ao processar QR:", error);
        }
    }
}

ExpenseQRScanner.template = "expense_qr.Scanner";

registry.category("actions").add("expense_qr_scanner", ExpenseQRScanner);