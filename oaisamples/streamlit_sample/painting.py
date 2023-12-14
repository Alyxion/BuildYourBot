tools_descriptions = [{
    "type": "function",
    "function": {
        "name": "paint_circle",
        "description": "Helper function to paint circles",
        "parameters": {
            "type": "object",
            "properties": {
                "color": {"type": "string", "description": "The color of the circle as hex code, e.g. #ff0000 for red"},
                "center": {
                    "type": "number",
                    "description": "The center of the circle as a string in the format x,y",
                },
                "radius": {
                    "type": "number",
                    "description": "The circles radius",
                },
            },
            "required": ["center", "radius"],
        },
    },
},
    {"type": "function",
     "function": {
         "name": "paint_line_string",
         "description": "Helper function to paint a line string of arbitrary length",
         "parameters": {
             "type": "object",
             "properties": {
                 "color": {"type": "string",
                           "description": "The color of the circle as hex code, e.g. #ff0000 for red"},
                 "coordinates": {
                     "type": "array",
                     "description": "The coordinates of the circle as a x, y pairs",
                     "items": {
                         "type": "array",
                         "items": {
                             "type": "number"
                         }
                     }
                 },
             }
         }
     }
     }
]

tools = tools_descriptions


def test_painting():
    from oaisamples.easy_bot import EasyChatbot
    prompt = ("You are a bot who helps the users with math. If required you can use the tool paint_lines to "
              "visualize lines or paint_circle to visualize circles. The painting area is from 0,0 to 1,1.")
    bot = EasyChatbot(system_prompt=prompt, tools=tools)
    # result = bot.run_completion("Hi, can you paint a yellow circle with a radius of 0.3?")
    result = bot.run_completion("Hi, can you paint a yellow circle and a blue triangle where the triangles coordinates"
                                "are on the circle's boundary?")
    # result = bot.run_completion("Hi, can you tell me how to calculate the area of a circle?")

    print(result.choices[0].message.content)

    print(result.usage.prompt_tokens)

    if result.choices[0].message.tool_calls is not None:
        for cur_tool in result.choices[0].message.tool_calls:
            print(cur_tool.function.name, cur_tool.function.arguments)




if __name__ == '__main__':
    test_painting()
