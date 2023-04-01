import openai
import json

key="<API KEY>"
openai.api_key = key

def generate_response(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        temperature = 0,
        max_tokens=256,
        prompt = "a textual hyper realistic videogame where everything is too realistic, that will punish the player if he tries the impossible or take too much time. The game is super hard and can not be won. The hyper realism can kill the fun. Examples: (>>> means the user, - means the game):\nexample1:\n-You wake up in a forest\n>>> climb a tree\n-You climb a tree. More forest.\n>>>look around\n-You look around, you see more forest.\n>>> head north\n-You head north. You are in a forest. It has been thirty minutes. Your mother is waiting at the airport.\n>>>keep heading north\n-You continue to head the north. It has been one hour. Dusk is falling near the airport. Your Mother will be in the shadow soon.\n>>>go to the west\n-You are out of the forest. There is a clearing.\n>>> go to the clearing.\n-You are in the clearing. You are no longer in the forest. And therefore the vampires won. The end.\n\nexample 2:-You wake up in a forest.\n>>> do nothing\n -You do nothing. It has been thirty minutes and you feel hungry.\n>>> wait\n -It has been one hour. You feel so hungry, you must eat or you could die.\n>>> find something to eat.\n-Actually you do not know what can be eaten in this forest, and there is risk that it can be poisoned.\n>>> hunt animals.\n -You try to find an animal, and you find a bear. You can not escape and you die. The end.)\n Now simulate the narrator by responding only to the last instruction '>>>' of the player with maximum two sentences. The player must survive after at least 6 instructions. If the player survived after ten instructions, you must find a realistic way that the player loosed the game, with at the end the sentence 'The end'. You must respond only to the last instruction, and do nothing more. Here is the latest historic:"+text
    )
    response = json.loads(str(response))
    rep=response["choices"][0]["text"]
    rep=rep[:rep.find("\n>>>")]
    return rep
def main_gpt():
    messages = "-You wake up in a forest."
    print(messages)
    response = ""
    while 1:
        prompt = input(">>> ")
        messages+="\n>>> "+prompt
        try:
            response = generate_response(messages)
        except Exception as err:
            print(err)
        messages+="\n"+response
        print(response)
        if "The end" in response:
            break

main_gpt()
