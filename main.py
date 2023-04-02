from flask import Flask, render_template, request, jsonify
from web3 import Web3


app = Flask(__name__)


class Contract_method:
    def __init__(self):
        self.contract_address = '0xC8042EAc54eFDf23ABC0657a48975eC815092B5d'
        self.abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_surname",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_GPAX",
				"type": "uint256"
			}
		],
		"name": "addStudent",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			}
		],
		"name": "deleteStudent",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_surname",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_GPAX",
				"type": "uint256"
			}
		],
		"name": "updateStudent",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getAllStudents",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "id",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "surname",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "gpax",
						"type": "uint256"
					},
					{
						"internalType": "bool",
						"name": "flag",
						"type": "bool"
					}
				],
				"internalType": "struct StudentRecords.Student[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			}
		],
		"name": "getStudentById",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "id",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "surname",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "gpax",
						"type": "uint256"
					},
					{
						"internalType": "bool",
						"name": "flag",
						"type": "bool"
					}
				],
				"internalType": "struct StudentRecords.Student",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
        self.Web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
        self.owner = self.Web3.eth.accounts[0]
        self.contract = self.Web3.eth.contract(
            address=self.contract_address, abi=self.abi)

    def get(self, st_id):
        return self.contract.functions.getStudentById(int(st_id)).call()

    def get_all(self):
        data = self.contract.functions.getAllStudents().call()
        object = []
        for i in range(len(data)):
            if data[i][4]:
                object.append({
                    'id': data[i][0],
                    'name': data[i][1],
                    'surname': data[i][2],
                    'gpax': float(data[i][3] / 100),
                    'flag': data[i][4]
                })
            else:
                pass

        return object

    def insert(self, name, surname, gpax):
        return self.contract.functions.addStudent(name, surname, gpax).transact({'from': self.owner})

    def update(self, st_id, name, surname, gpax):
        return self.contract.functions.updateStudent(st_id, name, surname, gpax).transact({'from': self.owner})

    def delete(self, st_id):
        return self.contract.functions.deleteStudent(st_id).transact({'from': self.owner})


Contract_method = Contract_method()


@app.route('/')
def index():
    data = Contract_method.get_all()
    return render_template('index.html', data=data)


@app.route('/addStudent', methods=['POST'])
def insert():
    obj = request.get_json()
    tx = Contract_method.insert(obj['name'], obj['surname'], int(obj['gpax']))
    return jsonify({"result": "success", 'tx': tx.hex()})


@app.route('/updateStudent', methods=['PUT'])
def update():
    obj = request.get_json()
    tx = Contract_method.update(
        int(obj['id']), obj['name'], obj['surname'], int(obj['gpax']))
    return jsonify({"result": "success", 'tx': tx.hex()})


@app.route('/deleteStudent', methods=['DELETE'])
def delete():
    obj = request.get_json()
    tx = Contract_method.delete(obj['id'])
    return jsonify({"result": "success", 'tx': tx.hex()})


@app.route('/getStudentById/<id>', methods=['GET'])
def get_by_id(id):
    data = Contract_method.get(id)
    return jsonify({'data': data})


@app.route('/getAllStudents', methods=['GET'])
def get():
    data = Contract_method.get_all()
    return jsonify({"result": "success", 'data': data})


if __name__ == '__main__':
    app.run(debug=True)
