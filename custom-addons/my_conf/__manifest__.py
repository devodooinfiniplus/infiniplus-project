{
    'name': 'Configuração de Base',
    'version': '1.0',
    'summary': 'Garante a permanência das apps nativas',
    'author': 'RSplus',
    'category': 'Extra Tools',
    'depends': [
        'base',
        'crm',           # Adicione o CRM aqui
        'sale_management', # Se usar Vendas
        'stock',         # Se usar Inventário
        'project',       # Se usar Projetos
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
