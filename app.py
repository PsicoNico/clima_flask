from flask import Flask, render_template, request
import requests
from googletrans import Translator

app = Flask(__name__)

def consultar_openweather(cidade):
    API_KEY = "abc60009f2745afda114c2d341591172"
    
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            descricao_ingles = data['weather'][0]['description']
            
            tradutor = Translator()
            descricao_portugues = tradutor.translate(descricao_ingles, src='en', dest='pt').text
            
            return {
                'descricao': descricao_portugues,
                'temperatura': f"{data['main']['temp']}°C",
                'umidade': f"{data['main']['humidity']}%",
                'pressao': f"{data['main']['pressure']} hPa",
                'velocidade_vento': f"{data['wind']['speed']} m/s"
            }
        else:
            return None
    except Exception as e:
        print(f"Erro ao consultar OpenWeather: {str(e)}")
        return None

@app.route('/', methods=['GET', 'POST'])
def consultar_clima():
    cidade = None
    data_clima = None
    
    if request.method == 'POST':
        cidade = request.form.get('cidade')
        
        if cidade:
            data_clima = consultar_openweather(cidade)
    
    return render_template('index.html', cidade=cidade, data_clima=data_clima)

if __name__ == '__main__':
    app.run(debug=True)

