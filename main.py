from f1gpt.f1_data import F1Event, F1Session
from f1gpt.prompts import (
    event_prompt,
    model,
    race_prompt,
    range_prompt,
    session_prompt)

if __name__ == "__main__":
    import sys 

    if 'event' in sys.argv:
        next_event = F1Event('Hungary')
        template = next_event.create_event_briefing()
        response = model.predict_messages(event_prompt.format_messages(event_info = template))
        print(response.content)
    elif 'session' in sys.argv:
        session = F1Session('Silverstone', 4)
        kwargs = session.session_briefing()
        response = model.predict_messages(session_prompt.format_messages(**kwargs))
        print(response.content)
    elif 'race' in sys.argv:
        session = F1Session('Silverstone', 5)
        kwargs = session.race_briefing()
        response = model.predict_messages(race_prompt.format_messages(**kwargs))
        print(response.content)
    elif 'range' in sys.argv:
        session = F1Session('Silverstone', 4)
        template = session.range_briefing([5300,5530], turn_name = '15')
        response = model.predict_messages(range_prompt.format_messages(range_info = template))
        print(response.content)    