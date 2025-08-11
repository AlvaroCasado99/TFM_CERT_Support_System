
def smishing_report_template(data, user, timestamp):
    def format_report_body(data, user, body, timestamp):
        page = body.replace("{{date}}", timestamp)
        page = page.replace("{{name}}", user['name'])
        page = page.replace("{{surname}}", user['surname'])
        page = page.replace("{{message}}", data['msg'])
        page = page.replace("{{flavour}}", data['flavour'])
        page = page.replace("{{campaign}}", data['campaign'])
        #page = page.replace("{{persons}}", "XXXX")
        page = page.replace("{{orgs}}", data['entity'] if data['entity'] else "-")
        page = page.replace("{{email}}", data['mail'] if data['mail'] else "-")
        page = page.replace("{{url}}", data['url'] if data['url'] else "-")
        page = page.replace("{{active}}", "Sí" if data['html'] else "No")
        return page

    template = """<!DOCTYPE html>
    <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Reporte de Smishing</title>
            <style>
                body {
                    font-family: "Segoe UI", sans-serif;
                    margin: 40px;
                    line-height: 1.6;
                    color: #333;
                }
                header {
                    border-bottom: 2px solid #007ACC;
                    padding-bottom: 10px;
                    margin-bottom: 30px;
                }
                .header-title {
                    font-size: 24px;
                    font-weight: bold;
                    color: #007ACC;
                }
                .subtitle {
                    font-size: 16px;
                    color: #555;
                }
                section {
                    margin-bottom: 25px
                }
                h2 {
                    border-left: 5px solid #007ACC;
                    padding-left: 10px;
                    font-size: 18px;
                    color: #007ACC;
                }
                .data-block {
                    background-color: #f3f3f3;
                    padding: 15px;
                    border-radius: 6px;
                    white-space: pre-wrap;
                }
                .footer {
                    font-size: 12px;
                    color: #888;
                    text-align: right;
                    margin-top: 40px;
                    border-top: 1px solid #ccc;
                    padding-top: 10px;
                }
                .label {
                    font-weight: bold;
                    color: #444;
                }
                .page-break {
                    page-break-before: always;
                    break-before: page;
                }
            </style>
        </head>
        <body>
            {{body}}
        </body>
    </html>"""

    body = """<header>
            <div class="header-title">GVIS - Proyecto LUCIA</div>
            <div class="subtitle">Centro de Respuesta ante Incidentes de Seguridad (CERT)</div>
        </header>

        <section>
            <h2>Información general</h2>
            <p><span class="label">Fecha del reporte:</span> {{date}}</p>
            <p><span class="label">Técnico responsable:</span> {{name}} {{surname}}</p>
            <p><span class="label">Identificador de campaña:</span> {{campaign}}</p>
        </section>

        <section>
            <h2>Mensaje sospechoso</h2>
            <div class="data-block">{{message}}</div>
        </section>

        <section>
            <h2>Clasificación del mensaje</h2>
            <p><span class="label">Tipo de smishing:</span> {{flavour}}</p>
        </section>

        <section>
            <h2>Entidades identificadas</h2>
            <!-- <p><span class="label">Personas:</span> {{persons}}</p> -->
            <p><span class="label">Organizaciones:</span> {{orgs}}</p>
        </section>

        <section>
            <h2>Indicadores técnicos</h2>
            <p><span class="label">Correos electrónicos detectados:</span> {{email}}</p>
            <p><span class="label">URL encontrada:</span> {{url}}</p>
            <p><span class="label">URL activa:</span> {{active}}</p>
        </section>

        <div class="footer">
            Proyecto LUCIA – GVIS | Documento interno – Confidencial
        </div>
    """

    page_break = """\n<div class="page-break"></div>\n"""

    if isinstance(data, list):
        pages = [format_report_body(d, user, body, timestamp) for d in data]
        joined_pages = page_break.join(pages)
        return template.replace("{{body}}", joined_pages)
    else:
        page = format_report_body(data, user, body, timestamp)
        return template.replace("{{body}}", page)
