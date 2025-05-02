# searchbot
# 1. Clone the repo
git clone https://github.com/yourusername/searchbot.git
cd searchbot

# 2. Set up a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your OpenAI API Key
export OPENAI_API_KEY="your-api-key"  # On Windows: set OPENAI_API_KEY=your-api-key

# 5. Run the app
python app.py
