from dotenv import load_dotenv

import scrum_bot

load_dotenv()

if __name__ == '__main__':
    app = scrum_bot(__name__)
    app.run(port=3000)
