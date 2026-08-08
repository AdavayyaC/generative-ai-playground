# evaluation_data = [

#     {
#         "question": "What did James Gosling say about AI tools?",
#         "ground_truth": (
#             "James Gosling said that he finds AI tools mostly annoying. "
#             "He believes they make difficult software problems worse "
#             "while only marginally improving easier problems."
#         )
#     },

#     {
#         "question": "What does James Gosling consider difficult about software development?",
#         "ground_truth": (
#             "He considers testing difficult because it is hard to know "
#             "whether software actually does what it is supposed to do."
#         )
#     },

#     {
#         "question": "Why does James Gosling think AI can make software development worse?",
#         "ground_truth": (
#             "He believes AI makes the hard problems worse while making "
#             "the easier and more enjoyable problems only marginally better."
#         )
#     },

#     {
#         "question": "What did James Gosling say about backward compatibility?",
#         "ground_truth": (
#             "He discussed backward compatibility as an important constraint "
#             "that makes designing and changing Java more difficult."
#         )
#     },

#     {
#         "question": "What is Project Valhalla?",
#         "ground_truth": (
#             "Project Valhalla is a long-running Java project involving "
#             "complex language and performance-related design problems."
#         )
#     }
# ]


evaluation_data = [

    {
        "question": "What did James Gosling say about AI tools?",
        "ground_truth": (
            "James Gosling said that he finds AI tools mostly annoying. "
            "He believes they make difficult software problems worse "
            "while only marginally improving easier problems."
        ),
        "relevant_text": "I have played with AI tools and I mostly find them to be really annoying."
    },

    {
        "question": "What does James Gosling consider difficult about software development?",
        "ground_truth": (
            "He considers testing difficult because it is hard to know "
            "whether software actually does what it is supposed to do."
        ),
        "relevant_text": (
            "How do you know that this piece of software actually does "
            "what you need it to do?"
        )
    },

    {
        "question": "Why does James Gosling think AI can make software development worse?",
        "ground_truth": (
            "He believes AI makes the hard problems worse while making "
            "the easier and more enjoyable problems only marginally better."
        ),
        "relevant_text": (
            "everything I've seen about AI tools just is that they just "
            "make the hard problem worse."
        )
    },

    {
        "question": "What did James Gosling say about backward compatibility?",
        "ground_truth": (
            "He discussed backward compatibility as an important constraint "
            "that makes designing and changing Java more difficult."
        ),
        "relevant_text": (
            "if performance matters or security matters or backwards "
            "compatibility matters, then all of a sudden these design "
            "problems become much more complex."
        )
    },

    {
        "question": "What is Project Valhalla?",
        "ground_truth": (
            "Project Valhalla is a long-running Java project involving "
            "complex language and performance-related design problems."
        ),
        "relevant_text": (
            "there's this recent thing called Project Valhalla."
        )
    }
]