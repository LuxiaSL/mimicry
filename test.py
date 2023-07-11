import json

# Load the questionnaire data from a JSON file
with open('questions.json', 'r') as file:
    questionnaire_data = json.load(file)

# Define the item lists for the subscales and broad factors
COGPER_ITEMS = [1, 3, 4, 9, 10, 12, 13, 18, 19, 21, 22, 27, 28, 30, 31, 36, 37, 39, 40, 44, 45, 47, 48, 52, 53, 55, 56, 59, 60, 61, 63, 64, 65]
INTERPER_ITEMS = [2, 6, 8, 9, 11, 15, 17, 18, 20, 24, 26, 27, 29, 33, 35, 36, 38, 41, 43, 44, 46, 49, 51, 52, 54, 57, 59, 62, 65, 66, 68, 71, 73]
DISORG_ITEMS = [5, 7, 14, 16, 23, 25, 32, 34, 42, 50, 58, 67, 69, 70, 72, 74]

IDEAS_OF_REFERENCE_ITEMS = [1, 10, 19, 28, 37, 45, 53, 60, 63]
EXCESSIVE_SOCIAL_ANXIETY_ITEMS = [2, 11, 20, 29, 38, 46, 54, 71]
ODD_BELIEFS_OR_MAGICAL_THINKING_ITEMS = [3, 12, 21, 30, 39, 47, 55]
UNUSUAL_PERCEPTUAL_EXPERIENCES_ITEMS = [4, 13, 22, 31, 40, 48, 56, 61, 64]
ODD_OR_ECCENTRIC_BEHAVIOR_ITEMS = [5, 14, 23, 32, 67, 70, 74]
NO_CLOSE_FRIENDS_ITEMS = [6, 15, 24, 33, 41, 49, 57, 62, 66]
ODD_SPEECH_ITEMS = [7, 16, 25, 34, 42, 50, 58, 69, 72]
CONSTRICTED_AFFECT_ITEMS = [8, 17, 26, 35, 43, 51, 68, 73]
SUSPICIOUSNESS_ITEMS = [9, 18, 27, 36, 44, 52, 59, 65]

# Function to calculate the total score and subscale scores
def calculate_scores(data):
    total_score = 0
    cogper_score = 0
    interper_score = 0
    disorg_score = 0
    ideas_of_reference_score = 0
    excessive_social_anxiety_score = 0
    odd_beliefs_or_magical_thinking_score = 0
    unusual_perceptual_experiences_score = 0
    odd_or_eccentric_behavior_score = 0
    no_close_friends_score = 0
    odd_speech_score = 0
    constricted_affect_score = 0
    suspiciousness_score = 0

    for item, response in data.items():
        if response.lower() == '1':
            total_score += 1
            if int(item) in COGPER_ITEMS:
                cogper_score += 1
            if int(item) in INTERPER_ITEMS:
                interper_score += 1
            if int(item) in DISORG_ITEMS:
                disorg_score += 1
            if int(item) in IDEAS_OF_REFERENCE_ITEMS:
                ideas_of_reference_score += 1
            if int(item) in EXCESSIVE_SOCIAL_ANXIETY_ITEMS:
                excessive_social_anxiety_score += 1
            if int(item) in ODD_BELIEFS_OR_MAGICAL_THINKING_ITEMS:
                odd_beliefs_or_magical_thinking_score += 1
            if int(item) in UNUSUAL_PERCEPTUAL_EXPERIENCES_ITEMS:
                unusual_perceptual_experiences_score += 1
            if int(item) in ODD_OR_ECCENTRIC_BEHAVIOR_ITEMS:
                odd_or_eccentric_behavior_score += 1
            if int(item) in NO_CLOSE_FRIENDS_ITEMS:
                no_close_friends_score += 1
            if int(item) in ODD_SPEECH_ITEMS:
                odd_speech_score += 1
            if int(item) in CONSTRICTED_AFFECT_ITEMS:
                constricted_affect_score += 1
            if int(item) in SUSPICIOUSNESS_ITEMS:
                suspiciousness_score += 1

    return {
        'Total Score': total_score,
        'Cognitive-Perceptual Score': cogper_score,
        'Interpersonal Score': interper_score,
        'Disorganized Score': disorg_score,
        'Ideas of Reference Score': ideas_of_reference_score,
        'Excessive Social Anxiety Score': excessive_social_anxiety_score,
        'Odd Beliefs or Magical Thinking Score': odd_beliefs_or_magical_thinking_score,
        'Unusual Perceptual Experiences Score': unusual_perceptual_experiences_score,
        'Odd or Eccentric Behavior Score': odd_or_eccentric_behavior_score,
        'No Close Friends Score': no_close_friends_score,
        'Odd Speech Score': odd_speech_score,
        'Constricted Affect Score': constricted_affect_score,
        'Suspiciousness Score': suspiciousness_score
    }

# Interpretations
def interpret_scores(scores):
    interpretation = ""

    # Total SPQ Score
    total_score = scores['Total Score']
    interpretation += f"Total SPQ Score: {total_score}\n"
    if total_score >= 42:
        interpretation += "Your total score indicates a higher presence of schizotypal traits. It's important to note that this questionnaire is not a diagnostic tool, but your score suggests a potential interest in exploring schizotypal characteristics further."

    # Broad Factors
    interpretation += "\nBroad Factors:\n"
    cogper_score = scores['Cognitive-Perceptual Score']
    interper_score = scores['Interpersonal Score']
    disorg_score = scores['Disorganized Score']
    interpretation += f"Cognitive-Perceptual Factor: {cogper_score}\n"
    interpretation += f"Interpersonal Factor: {interper_score}\n"
    interpretation += f"Disorganized Factor: {disorg_score}\n"

    # Subscales
    interpretation += "\nSubscales:\n"
    ideas_of_reference_score = scores['Ideas of Reference Score']
    excessive_social_anxiety_score = scores['Excessive Social Anxiety Score']
    odd_beliefs_or_magical_thinking_score = scores['Odd Beliefs or Magical Thinking Score']
    unusual_perceptual_experiences_score = scores['Unusual Perceptual Experiences Score']
    odd_or_eccentric_behavior_score = scores['Odd or Eccentric Behavior Score']
    no_close_friends_score = scores['No Close Friends Score']
    odd_speech_score = scores['Odd Speech Score']
    constricted_affect_score = scores['Constricted Affect Score']
    suspiciousness_score = scores['Suspiciousness Score']

    interpretation += f"Ideas of Reference: {ideas_of_reference_score}\n"
    interpretation += f"Excessive Social Anxiety: {excessive_social_anxiety_score}\n"
    interpretation += f"Odd Beliefs or Magical Thinking: {odd_beliefs_or_magical_thinking_score}\n"
    interpretation += f"Unusual Perceptual Experiences: {unusual_perceptual_experiences_score}\n"
    interpretation += f"Odd or Eccentric Behavior: {odd_or_eccentric_behavior_score}\n"
    interpretation += f"No Close Friends: {no_close_friends_score}\n"
    interpretation += f"Odd Speech: {odd_speech_score}\n"
    interpretation += f"Constricted Affect: {constricted_affect_score}\n"
    interpretation += f"Suspiciousness: {suspiciousness_score}\n"

    # Specific interpretations based on score values
    if total_score <= 12:
        interpretation += "Your total score falls within the lower range, suggesting a relatively lower presence of schizotypal traits."
    elif total_score >= 41:
        interpretation += "Your total score falls within the higher range, indicating a relatively higher presence of schizotypal traits. It's important to note that this questionnaire is not a diagnostic tool, but your score suggests a potential interest in exploring schizotypal characteristics further."

    if cogper_score >= 10:
        interpretation += "\nYour score in the Cognitive-Perceptual factor suggests a tendency to experience unusual perceptual phenomena, odd thoughts, and beliefs."

    if interper_score >= 10:
        interpretation += "\nYour score in the Interpersonal factor indicates difficulty with interpersonal relationships and social interactions. You may experience social anxiety, discomfort, or have limited close friendships."

    if disorg_score >= 5:
        interpretation += "\nYour score in the Disorganized factor reflects disorganized thinking, speech, or behavior. You may exhibit eccentric or odd behaviors that are perceived as unusual by others."

    interpretation += "\nSubscale Interpretations:\n"
    if ideas_of_reference_score >= 5:
        interpretation += "\nYour score in Ideas of Reference suggests a tendency to interpret neutral events as personally significant or having special meaning to oneself."

    if excessive_social_anxiety_score >= 5:
        interpretation += "\nYour score in Excessive Social Anxiety indicates heightened anxiety in social situations, leading to discomfort or avoidance."

    if odd_beliefs_or_magical_thinking_score >= 5:
        interpretation += "\nYour score in Odd Beliefs or Magical Thinking suggests the endorsement of unusual or idiosyncratic beliefs or beliefs in magical or supernatural phenomena."

    if unusual_perceptual_experiences_score >= 5:
        interpretation += "\nYour score in Unusual Perceptual Experiences indicates experiences of perceptual phenomena that may be uncommon or unconventional, such as illusions or hallucinations."

    if odd_or_eccentric_behavior_score >= 5:
        interpretation += "\nYour score in Odd or Eccentric Behavior suggests engaging in behaviors perceived as eccentric or unconventional by others."

    if no_close_friends_score >= 5:
        interpretation += "\nYour score in No Close Friends indicates a lack of close friendships or limited social connections."

    if odd_speech_score >= 5:
        interpretation += "\nYour score in Odd Speech suggests unconventional speech patterns, including unusual word usage, idiosyncratic expressions, or peculiar intonation."

    if constricted_affect_score >= 5:
        interpretation += "\nYour score in Constricted Affect indicates limited emotional expressiveness or reduced range of emotional responses."

    if suspiciousness_score >= 5:
        interpretation += "\nYour score in Suspiciousness suggests a heightened level of suspiciousness or mistrust toward others."

    return interpretation

# Example usage:
user_responses = {}
"""
for item, question in questionnaire_data.items():
    response = input(f'{question} (Enter "1" or "0"): ')
    user_responses[item] = response

scores = calculate_scores(user_responses)"""

interpretation = interpret_scores({
        'Total Score': 51,
        'Cognitive-Perceptual Score': 25,
        'Interpersonal Score': 19,
        'Disorganized Score': 12,
        'Ideas of Reference Score': 8,
        'Excessive Social Anxiety Score': 6,
        'Odd Beliefs or Magical Thinking Score': 6,
        'Unusual Perceptual Experiences Score': 6,
        'Odd or Eccentric Behavior Score': 7,
        'No Close Friends Score': 6,
        'Odd Speech Score': 5,
        'Constricted Affect Score': 2,
        'Suspiciousness Score': 5
    })

# Display the interpretations
print("Interpretations:\n")
print(interpretation)

