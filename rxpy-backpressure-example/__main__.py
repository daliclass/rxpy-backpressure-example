from rx.concurrency import NewThreadScheduler
from rx.core.typing import Observer
from rx import interval
from time import sleep

from rx.subjects import Subject
from rxpy_backpressure import BackPressure


class AddNameSubject(Subject):

    def on_next(self, value) -> None:
        some_dict = dict()
        some_dict['name'] = "Joe Blogs"
        some_dict['interval'] = value
        super(AddNameSubject, self).on_next(some_dict)


class AddScoreSubject(Subject):

    def on_next(self, value: dict) -> None:
        sleep(2)
        value['score'] = 1
        super(AddScoreSubject, self).on_next(value)


class ConsumerObserver(Observer):

    def on_next(self, value: dict) -> None:
        print(value)

    def on_error(self, error: Exception) -> None:
        pass

    def on_completed(self) -> None:
        pass


scheduler = NewThreadScheduler()
add_name_subject = AddNameSubject()
add_score_subject = AddScoreSubject()
consumer_observer = ConsumerObserver()

interval(1).subscribe(add_name_subject, scheduler)
add_name_subject.subscribe(BackPressure.LATEST(add_score_subject), scheduler)
add_score_subject.subscribe(consumer_observer, scheduler)

input("Press any key to quit\n")
