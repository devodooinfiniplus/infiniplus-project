/** @odoo-module **/

import { Component, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";

const jsQR = window.jsQR;

export class QRScanner extends Component {
    setup() {
        this.videoRef = useRef("video");
        this.canvas = document.createElement("canvas");
        this.stream = null;
        this.running = true;

        onMounted(async () => {
            try {
                this.stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: "environment" },
                });
                this.videoRef.el.srcObject = this.stream;
                await this.videoRef.el.play();
                this.scan();
            } catch (err) {
                console.error("Erro ao aceder à câmara:", err);
            }
        });

        onWillUnmount(() => {
            this.running = false;
            if (this.stream) {
                this.stream.getTracks().forEach(track => track.stop());
            }
        });
    }

    scan() {
        if (!this.running) {
            return;
        }

        const video = this.videoRef.el;
        if (video && video.readyState === video.HAVE_ENOUGH_DATA) {
            this.canvas.width = video.videoWidth;
            this.canvas.height = video.videoHeight;

            const ctx = this.canvas.getContext("2d");
            ctx.drawImage(video, 0, 0, this.canvas.width, this.canvas.height);

            const imageData = ctx.getImageData(
                0,
                0,
                this.canvas.width,
                this.canvas.height
            );

            const code = jsQR(
                imageData.data,
                imageData.width,
                imageData.height
            );

            if (code && code.data) {
                this.running = false;

                if (this.stream) {
                    this.stream.getTracks().forEach(track => track.stop());
                }

                // ACTION CORRETA PARA ODOO 17/18
                this.env.services.action.doAction({
                    type: "ir.actions.act_window",
                    name: "Scan QR Invoice",
                    res_model: "qr.invoice.wizard",
                    views: [[false, "form"]],
                    target: "new",
                    context: {
                        default_qr_data: code.data,
                    },
                });

                return;
            }
        }

        requestAnimationFrame(this.scan.bind(this));
    }
}

QRScanner.template = "vendor_qr_invoice.QRScannerTemplate";
registry.category("actions").add("qr_scanner_action", QRScanner);
