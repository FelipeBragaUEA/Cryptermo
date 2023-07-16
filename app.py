from flask import Flask, render_template, request
import datetime
import hashlib
import random

app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, data, previous_hash, validator):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.validator = validator
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.validator)
        return hashlib.sha256(data.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0", None)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


class ProofOfStake:
    def __init__(self, validators):
        self.validators = validators

    def select_validator(self):
        total_stake = sum([validator['stake'] for validator in self.validators])
        random_number = random.uniform(0, total_stake)
        cumulative_stake = 0

        for validator in self.validators:
            cumulative_stake += validator['stake']
            if cumulative_stake >= random_number:
                return validator

        return None


blockchain = Blockchain()

# Sample validators with stake amounts
validators = [
    {'name': 'Validator 1', 'stake': 10},
    {'name': 'Validator 2', 'stake': 5},
    {'name': 'Validator 3', 'stake': 3},
]

proof_of_stake = ProofOfStake(validators)

@app.route('/')
def index():
    return render_template('index.html', chain=blockchain.chain)

@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.form['data']
    selected_validator = proof_of_stake.select_validator()
    new_block = Block(len(blockchain.chain), datetime.datetime.now(), data, "", selected_validator)
    blockchain.add_block(new_block)
    return render_template('index.html', chain=blockchain.chain)

if __name__ == '__main__':
    app.run(debug=True)
