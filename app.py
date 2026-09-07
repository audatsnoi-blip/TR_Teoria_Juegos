from flask import Flask, render_template, request
import main

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def inicio():

    evolucio = None

    if request.method == "POST":

        jugadors_per_estrategia = int(
            request.form["jugadors_per_estrategia"]
        )

        rondes_per_partida = int(
            request.form["rondes_per_partida"]
        )

        generacions = int(
            request.form["generacions"]
        )

        jugadors_eliminats = int(
            request.form["jugadors_eliminats"]
        )

        # Executar la simulació
        evolucio = main.executar_simulacio(
            jugadors_per_estrategia,
            rondes_per_partida,
            generacions,
            jugadors_eliminats
        )

        # Ordenar les estratègies de més a menys jugadors
        evolucio = [
            dict(
                sorted(
                    poblacio.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
            )
            for poblacio in evolucio
        ]

    return render_template(
        "index.html",
        evolucio=evolucio
    )


if __name__ == "__main__":
    app.run(debug=True)