from flask import Flask, render_template, request, redirect, url_for
import datetime
import hashlib

app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(data.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

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

blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html', chain=blockchain.chain)

@app.route('/lab_results')
def lab_results():
    return render_template('lab_results.html', chain=blockchain.chain)

@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.form['data']
    new_block = Block(len(blockchain.chain), datetime.datetime.now(), data, "")
    blockchain.add_block(new_block)
    return render_template('index.html', chain=blockchain.chain)

@app.route('/save_profile', methods=['POST'])
def save_profile():
    name = request.form.get('name')
    dob = request.form.get('dob')
    address = request.form.get('address')
    family_history = request.form.getlist('family-history')
    personal_history = request.form.getlist('personal-history')

    # Update the Lab Results page with profile and health history information
    profile_data = f"Name: {name}\nDate of Birth: {dob}\nAddress: {address}"
    history_data = ""

    if family_history:
        history_data += "Family Health History:\n"
        history_data += "\n".join(family_history)
        history_data += "\n\n"
    if personal_history:
        history_data += "Personal Health History:\n"
        history_data += "\n".join(personal_history)

    combined_data = profile_data + "\n" + history_data

    new_block = Block(len(blockchain.chain), datetime.datetime.now(), combined_data, "")
    blockchain.add_block(new_block)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)