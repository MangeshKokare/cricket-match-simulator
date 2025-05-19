# 🏏 Cricket Match Simulator
A Streamlit web app that simulates a cricket match ball-by-ball between two teams. The simulation uses player skill factors, chance of extras, and wicket probabilities to create a dynamic and realistic match experience.

🚀 Features
Live ball-by-ball commentary
Real-time scorecard and stats
Player-based skill impact
Chance of extras (wide, no-ball)
Wicket probability with bowler stats
Easy to use Streamlit UI

🛠 How It Works
User enters team names and player details.
Match is simulated over a fixed number of overs.
Commentary and scorecard update in real time.
Final result and player stats are displayed.


🔧 App Functionality Overview
This app simulates a short-format cricket match (5 overs) between two user-selected teams. Below are the key components and what each part does:

🧩 1. Team and Player Selection
Users select two teams and assign 5 players per team.
Each team has a unique lineup for batting and bowling.

![image](https://github.com/user-attachments/assets/a0d6cbb1-42e9-4021-beb5-fb5a964e202d)


🎛️ 2. Skill and Match Factor Inputs
Players can adjust:
Player Skill Factor (higher = better performance)
Chance of Extra Runs (probability of wides/no-balls)
Wicket Base Modifier (affects chances of wickets falling)
These factors influence match outcomes dynamically.

![image](https://github.com/user-attachments/assets/97ee761d-dd10-4758-875a-ecf6c91dcf31)


🏏 3. Match Simulation
Users click a "Start Match" button to begin the simulation.
The app simulates:
Ball-by-ball commentary
Overs progression
Wickets, extras, sixes, and other outcomes
Match is played for selected overs or until 10 wickets fall.

![image](https://github.com/user-attachments/assets/3198905e-a78f-4539-ac93-54f0043db784)



📊 4. Live Commentary
Displays each ball’s outcome in a real-time text area:
Example: 📌 Over 2.2 → Action: Six, Runs: 6

![image](https://github.com/user-attachments/assets/34abbf9c-a4e8-4fa5-995a-f9cf70d82c67)


📋 5. Scorecard Display
Shows final scores after each innings.
Includes:
Total Runs, Wickets, Overs
Individual batsman scores
Bowler stats (wickets taken and overs bowled)

![image](https://github.com/user-attachments/assets/1b8f4aec-3528-49f5-8c22-90e99be91842)



🔁 6. Second Innings and Winner Declaration
Once the second team finishes batting, the app:
Compares scores
Declares the winner or tie
Displays a final summary

![image](https://github.com/user-attachments/assets/0d9160cc-62b7-429b-b7e9-4b6e54837b74)


![image](https://github.com/user-attachments/assets/5a54cbe8-85d3-4ba3-af66-3b679b42a99f)
