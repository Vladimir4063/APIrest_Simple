from flask import Flask, json, jsonify, request

#El request: proporciona los datos que estan enviando por http

app = Flask(__name__)

from products import products #llamamos productos

#Testing rout
@app.route('/ping', methods = ['GET'])
def ping():
    return jsonify({'response': 'Pong!'}) 

#Get data routes
@app.route('/products')
def getProducts():
    #return jsonify(products)
    return jsonify({'products': products}) #send list

@app.route('/products/<string:product_name>')
def getProduct(product_name):
    #print(product_name)
    #return 'recibido'
    productsFound = [product for product in products if product['name'] == product_name.lower()] #Cuando lo encuentre, enviara datos
    if (len(productsFound) > 0): #Si la cantidad de productos en la lista es mayor a 0, imprimela
        return jsonify({'product': productsFound[0]})
    return jsonify ({"message": "Product not found"}) #Si no hay valor en lista, envia informe

#Post/Add product
#Create Data Routes
@app.route('/products', methods= ['POST']) #Add products
def addProduct():
    #print(request.json)
    new_product = {
        "name" : request.json['name'],
        "price" : request.json['price'],
        "quantity" : request.json['quantity']
    }

    products.append(new_product)
    print("Product received")
    return jsonify({"message": "Product Added Succesfully", "products": products})

#Actualizar datos por ruta
#Update Date Route
@app.route('/products/<string:product_name>', methods = ['PUT'])
def editProduct(product_name):
    productFound = [product for product in products if product['name'] == product_name]
    if (len(productFound) > 0):
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json['quantity']
        print("Product Update")
        return jsonify({
            "message": "Produc Update",
            "product": productFound[0],
            "products" : products
        })
    return jsonify({
        "message": "Product not found"
    })

@app.route('/products/<string:product_name>', methods = ['DELETE'])
def deleteProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if len(productsFound) > 0:
        products.remove(productsFound[0])
        return jsonify({
            "message": "Product Deleted",
            "products": products
        })
    return jsonify({"message": "Product Not found"})


if __name__ == '__main__':
    app.run(debug=True, port=4000)

