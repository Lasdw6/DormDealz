from flask import Flask, render_template, request

import json
import requests
app = Flask(__name__)

@app.route('/')
def search_page():
  return render_template('hi.html')

@app.route('/recipes')
def get_recipes():
      return render_template('hi.html')
  
@app.route('/recipe')
def get_recipe():
    return render_template('hi.html')


if __name__ == '__main__':
  app.run(debug=True)