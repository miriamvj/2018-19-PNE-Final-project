import http.server
import socketserver
import json
import http.client

PORT = 8000
socketserver.TCPServer.allow_reuse_address = True
SERVER = 'rest.ensembl.org'


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == '/':
            f = open("form.html")
            content = f.read()
        elif "listSpecies" in self.path:
            SERVER = 'rest.ensembl.org'
            PORT = 80
            conn = http.client.HTTPConnection(SERVER, PORT)
            conn.request("GET", "/info/species?content-type=application/json")

            r1 = conn.getresponse()

            data = r1.read().decode('utf-8')
            general = json.loads(data)

            lista_genial = list()

            if 'limit' in self.path:
                lim = self.path.split('=')
                limit = lim[1]
                if limit == '':
                    for index in general['species']:
                        hola = index['name']
                        lista_genial.append(hola)
                    content = """<!DOCTYPE html>
                                    <html lang="en">
                                    <head>
                                        <meta charset="UTF-8">
                                        <title>List of species.:</title>
                                    </head>
                                    <body style="background-color: lightgreen;">
                                        <h1>List of species:</h1>
                                        <p>{}</p>
                                        <a href="/">Main page</a>
                                    </body>
                                    </html.>"""
                    content = content.format(lista_genial)
                else:
                    try:
                        limit = int(lim[1])
                        for index in general['species'][:limit]:
                            hola = index['name']
                            lista_genial.append(hola)
                        content = """<!DOCTYPE html>
                                                            <html lang="en">
                                                            <head>
                                                                <meta charset="UTF-8">
                                                                <title>List of species.:</title>
                                                            </head>
                                                            <body style="background-color: lightgreen;">
                                                                <h1>List of species:</h1>
                                                                <p>{}</p>
                                                                <a href="/">Main page</a>
                                                            </body>
                                                            </html.>"""
                        content = content.format(lista_genial)
                    except ValueError:
                        f = open("error.html")
                        content = f.read()
            else:
                for index in general['species']:
                    hola = index['name']
                    lista_genial.append(hola)
                content = """<!DOCTYPE html>
                                                                        <html lang="en">
                                                                        <head>
                                                                            <meta charset="UTF-8">
                                                                            <title>List of species.:</title>
                                                                        </head>
                                                                        <body style="background-color: lightgreen;">
                                                                            <h1>List of species:</h1>
                                                                            <p>{}</p>
                                                                            <a href="/">Main page</a>
                                                                        </body>
                                                                        </html.>"""
                content = content.format(lista_genial)


        elif "karyotype" in self.path:
            try:
                SERVER = 'rest.ensembl.org'
                PORT = 80
                conn = http.client.HTTPConnection(SERVER, PORT)
                lim = self.path.split('=')
                limit = lim[1]
                variable = "/info/assembly/" + limit + "?content-type=application/json"
                conn.request("GET", variable)

                r1 = conn.getresponse()

                data = r1.read().decode('utf-8')
                general = json.loads(data)
                hello = general['karyotype']

                if limit == '':
                    f = open("error.html")
                    content = f.read()
                else:
                    content = """<!DOCTYPE html>
                                                    <html lang="en">
                                                    <head>
                                                        <meta charset="UTF-8">
                                                        <title>Karyotype of a specie.:</title>
                                                    </head>
                                                    <body style="background-color: lightblue;">
                                                        <h1>Karyotype information:</h1>
                                                        <p>{}</p>
                                                        <a href="/">Main page</a>
                                                    </body>
                                                    </html.>"""
                    content = content.format(hello)
            except KeyError:
                f = open("error.html")
                content = f.read()
        elif "chromosomeLength" in self.path:
            try:
                lim = self.path.split('=')
                chromosome = lim[2]
                lim2 = lim[1].split('&')
                specie = lim2[0]

                PORT = 80
                SERVER = 'rest.ensembl.org'
                conn = http.client.HTTPConnection(SERVER, PORT)
                variable = "/info/assembly/" + specie + "/" + chromosome + "?content-type=application/json"
                conn.request("GET", variable)

                r1 = conn.getresponse()

                data = r1.read().decode('utf-8')
                general = json.loads(data)
                level = general['length']

                if specie == '':
                    f = open("error.html")
                    content = f.read()
                else:
                    content = """<!DOCTYPE html>
                                                                        <html lang="en">
                                                                        <head>
                                                                            <meta charset="UTF-8">
                                                                            <title>Length of a chromosome.:</title>
                                                                        </head>
                                                                        <body style="background-color: pink;">
                                                                            <h1>Length of the chosen chromosome:</h1>
                                                                            <p>{}</p>
                                                                            <a href="/">Main page</a>
                                                                        </body>
                                                                        </html.>"""
                    content = content.format(level)

            except KeyError:
                f = open("error.html")
                content = f.read()
            except IndexError:
                f = open("error.html")
                content = f.read()

        else:
            f = open("error.html")
            content = f.read()

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(content)))
        self.end_headers()

        # -- Sending the body of the response message
        self.wfile.write(str.encode(content))


# -- Main program
with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT: {}".format(PORT))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()