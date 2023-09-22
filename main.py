from f1gpt.briefiers import SessionBriefer
from f1gpt.connectors import F1Event, F1Session, drivers
from f1gpt.ploters import Ploter
from f1gpt.prompts import (
    event_prompt,
    model,
    race_prompt,
    range_prompt,
    session_prompt)

if __name__ == "__main__":
    import sys

    if 'event' in sys.argv:
        next_event = F1Event('Suzuka')
        response = model.predict_messages(event_prompt.format_messages(event_info = next_event.event))
        print(response.content)
    elif 'session' in sys.argv:
        session_number = sys.argv[sys.argv.index('session') + 1]
        session = F1Session('Suzuka', session_number, drivers)
        briefer = SessionBriefer(session)
        kwargs = briefer.create_session_brief()
        response = model.predict_messages(session_prompt.format_messages(**kwargs))
        print(response.content)
        ploter = Ploter(session)
        ploter.plot_comparison()
    elif 'race' in sys.argv:
        session = F1Session('Suzuka', 5, drivers)
        briefer = SessionBriefer(session)
        kwargs = briefer.create_race_brief()
        response = model.predict_messages(race_prompt.format_messages(**kwargs))
        print(response.content)
    elif 'range' in sys.argv:
        index = sys.argv.index('range')
        session_number = sys.argv[index + 1]
        range_start = int(sys.argv[index + 2])
        range_end = int(sys.argv[index + 3])
        lap_section = [range_start, range_end]
        session = F1Session('Suzuka', session_number, drivers)
        briefer = SessionBriefer(session)
        template = briefer.create_range_briefing(lap_section, turn_name = 'chincane')
        response = model.predict_messages(range_prompt.format_messages(range_info = template))
        print(response.content)
        ploter = Ploter(session)
        ploter.plot_comparison(chart_range=lap_section,
                               features= ['Speed', 'Brake', 'Throttle'])  
                               