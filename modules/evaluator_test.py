from evaluator import Evaluator

ev = Evaluator()


print(ev.value_evaluation("alarming"))
print(ev.novelty_evaluation("UPDATE 1-Harbinger hedge fund to run board slate at Ryerson"))
print(ev.novelty_evaluation("Saddam's daughter attends protest")) #from reuters
print(ev.novelty_evaluation("Saddam's girl shows up protest"))
print(ev.novelty_evaluation("More exemplary textiles can be found"))
print(ev.novelty_evaluation("A striking resemblance?"))
print(ev.novelty_evaluation("Annie Kaibovitz exposed on dog"))
print(ev.novelty_evaluation("Apple posts options expenses, stands by CEO Jobs"))
print(ev.novelty_evaluation("Yemen: ex-President Saleh offers talks to Saudi-led coalition"))
print(ev.novelty_evaluation("Visitors today flock to Venice to pay homage to the sumptuous textiles of the city’s sartorial reign. "))
print(ev.novelty_evaluation("The archives at the factory of Bevilacqua include 3,500 original designs"))
print(ev.novelty_evaluation("More exemplary textiles can be found in the former apartment of the Austrian Empress Elisabeth, at the Museo Correr on Piazza San Marco"))