from flask import Flask, request, jsonify
@app.route("/test", methods=["GET"])
def test():
        """
        Risponde inviando un json
        """
        return jsonify(
        {
            "id" : "ai",
            "response" : "Prova" 
        }
    )
if __name__ == "__main__" : 
    app.run(port=9000, debug=False)