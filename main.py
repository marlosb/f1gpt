from f1gpt.briefiers import SessionBriefer
from f1gpt.connectors import F1Event, F1Session, drivers
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
        response = model.predict_messages(event_prompt.format_messages(event_info = next_event.event))
        print(response.content)
    elif 'session' in sys.argv:
        session = F1Session('Hungary', 1, drivers)
        briefer = SessionBriefer(session)
        kwargs = briefer.create_session_brief()
        response = model.predict_messages(session_prompt.format_messages(**kwargs))
        print(response.content)
    elif 'race' in sys.argv:
        session = F1Session('Silverstone', 5, drivers)
        briefer = SessionBriefer(session)
        kwargs = briefer.create_race_brief()
        response = model.predict_messages(race_prompt.format_messages(**kwargs))
        print(response.content)
    elif 'range' in sys.argv:
        session = F1Session('Silverstone', 4, drivers)
        briefer = SessionBriefer(session)
        template = briefer.range_briefing([5300,5530], turn_name = '15')
        response = model.predict_messages(range_prompt.format_messages(range_info = template))
        print(response.content)    