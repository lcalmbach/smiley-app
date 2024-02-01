INFO = """# Smiley-App
Smiley-Geschwindigkeitsanzeigen sind ein innovatives Instrument zur Erhöhung der Verkehrssicherheit. Diese Anzeigen wechseln zwischen der dargestellten Geschwindigkeit und einem Emoticon, das Lob oder Tadel ausdrückt (😃 für das Einhalten des Tempolimits, 😡 bei dessen Überschreitung). Dies erfolgt auf eine nicht-bestrafende und freundliche Weise. Seit Anfang Februar 2023 sind 20 dieser neuen Geräte im Einsatz. Sie sind flexibel einsetzbar und durch ihre batteriebetriebene Stromversorgung an verschiedenen Orten aufstellbar. Bei der Auswahl der insgesamt 75 Standorte lag der Fokus besonders auf sensiblen Bereichen wie Kindergärten, Schulen und Altersheimen. Diese Standorte wurden nach einer umfassenden Evaluation, unter Einbeziehung von Fachleuten aus der Kantonsverwaltung und Rückmeldungen aus der Bevölkerung, festgelegt.

Die 20 Smiley-Geschwindigkeitsanzeigen rotieren zwischen den 75 Standorten und werden an jedem Ort für etwa fünf Monate aufgestellt. Dabei wird jeweils die Geschwindigkeit vor und nach dem Messstandort erfasst. Eine Messperiode besteht aus einer Vormessungsphase (1 Monat), der Betriebsphase (3 Monate) und einer Nachmessungsphase (1 Monat). Während der Vor- und Nachmessung werden die Geschwindigkeiten ohne Anzeige erfasst, in der Betriebsphase wird den Fahrerinnen und Fahrern ihre Einfahrtsgeschwindigkeit, begleitet von einem Emoticon, angezeigt. Mit diesen Messungen lässt sich die Effektivität der Smiley-Anzeige während des Betriebs sowie eine etwaige Nachwirkung auf das Fahrverhalten durch die Nachmessung analysieren. [Mehr Informationen finden Sie in der Medienmitteilung des JSD des Kantons Basel-Stadt.](https://www.jsd.bs.ch/nm/2023-start-des-betriebs-der-neuen-praeventiven-smiley-geschwindigkeitsanzeigen---ab-maerz-2023-aktiv-jsd.html)

**Datenaufbereitung und Ausreisser-Werte**

Die Rohdaten, die von diesen Geräten gesammelt wurden, sind öffentlich zugänglich auf dem [OGD-Portal](https://data.bs.ch/explore/dataset/100268) des Kantons Basel-Stadt. Bei der Durchsicht dieser Daten fällt auf, dass einige unrealistisch hohe Geschwindigkeiten, wie z.B. 231 km/h in einer 20 km/h-Zone, gemessen wurden. Diese extreme Werte sind mir grosser Wahrscheinlichkeit Messfehler und werden als Ausreisser bezeichnet. Sie sind statistisch nicht relevant, stören aber bei der graphischen Darstellung. Mit einem statistischen Verfahren wurden für jeden Standort alle Werte entfernt, welche mehr als 3 Standardabweichungen vom Mittelwert entfernt sind. Diese Geschwindigkeiten haben eine Wahrscheinlichkeit von 0.13%.

**Analyse der Einzelmessungen**
Der Datensatz von 2023 besteht aus über 6 Mio Einzelmessungen an 35 Standorten. Diese grosse Datenmenge bedeutet eine Herausforderung für eine aussagekräftige Analyse. Die grafischen und numerischen Methoden der Applikation smiley-app macht folgende Annahmen und versucht sie mit den Daten zu überprüfen:
- In der Vormessung und Nachmessung unterscheidet sich die Geschwindigkeit der Fahrzeuge bei der Einfahrt und Ausfahrt nicht systeematisch, da die Anzeige nicht aktiv ist.
- Im Betrieb ist die Geschwindigkeit der Fahrzeuge bei der Einfahrt höher als bei der  Ausfahrt, da die Anzeige aktiv ist, und zu schnelle Fahrende ihr Tempo nach einer 😡 Anzeige reduzieren. Es wird erwartet, dass dieser Effekt vor allem bei Fahrzeugen auftritt, schnell fahren, weshalb die 85-Perzentil Geschwindigkeit stärker reduziert wird als der Median.
- Die Geschwindigkeiten sind in der Vormessung am höchsten und Zu- und Abnahme der Geschwindigkeit am Smiley Standort sind zufällig, da die Anzeige ja noch nicht aktiv ist und es für die Fahrenden keinen Anlass gibt, die Geschwindigkeit am Standort zu reduzieren. Im Betrieb wird die Geschwindigkeit von Einfahrt zu Ausfahrt reduziert und zwar am stärksten bei hohen Geschwindigkeiten. In der Nachmessung wird erwartet, dass ein Teil der Fahrenden, welche die Strecke regelmässig befahren, ihr Tempo aus Gewohnheit der letzten 3 Monate reduzieren und es ist eine Geschwindigkeitsabnahme gegenüber der Vormessung zu erwarten, jedoch nicht so stark wie im Betrieb. Zudem sollte die Einfahrts und Ausfahrtsgeschwindigkeit wieder ähnlich sein, da die Anzeige nicht mehr aktiv ist.

**Statistiken**

Die Kennzahlen, die uns bei der Überprüfung der obigen Annahmen helfen sind:
- Median der Differenz von Ausfahrts- und Einfahrts-Geschwindigkeit
- 85-Perzentil der Differenz von Ausfahrts- und Einfahrts-Geschwindigkeit: Geschwindigkeit der schnellsten 15% der Fahrzeuge
- Anzahl Geschwindigkeitsübertretungen
- Median der Geschwindigkeitsübertretungen
- 85-Perzentil der Geschwindigkeitsübertretungen

**Analyse-Möglicheiten**

Die App verzichtet auf vorgefertigte Analysen und bietet dem User stattdessen verschiedene Werkzeuge, um die Daten selbst zu erkunden.
- Im Menü *Karten* kannst du die Daten geografisch darstellen und eine ausgewählte Kennzahl mit proportionaler Größe für jeden Standort anzeigen.
- Die Statistiken ermöglichen es dir, die Kennzahlen für die verschiedenen Standorte numerisch zu vergleichen. Der Reiter *Beschreibung Erwartungen* gibt Hinweise darauf, welche Resultate zu erwarten wären, wenn die erhoffte Annahme – nämlich dass die Geschwindigkeit im Betrieb reduziert wird und in der Nachmessung noch eine gewisse Nachwirkung eintritt – zutrifft. Die Beschreibung der Resultate fasst die numerischen Ergebnisse in Worten zusammen.
- Das Menü *Vergleich Ein-/Ausfahrt* vergleicht die Ein- und Ausfahrtsgeschwindigkeiten mit verschiedenen Grafiken, welche die Verteilung der beiden Geschwindigkeiten darstellen. Es können höchstens 10 Standorte gleichzeitig angezeigt werden. Im Dropdown-Feld *Standorte* kann die Auswahl der Standorte verändert werden. Ohne Auswahl werden die ersten 10 Standorte angezeigt. Werden nur ein oder zwei Standorte ausgewählt, so kann auch ein X-Y-Plot der beiden Geschwindigkeiten erstellt werden. Dieser erlaubt es, weitere Informationen aus den Daten zu ziehen, z.B. wird deutlich, dass bestimmte Geschwindigkeiten nie gemessen werden, wie z.B. 21 und 22 km/h bei der Einfahrt und 21 km/h bei der Ausfahrt. 
- Das Menü 'Analyse Standort' bietet umfassende Informationen zur Analyse eines spezifischen Standorts. Das Menü ermöglicht nicht nur den Vergleich von Ein- und Ausfahrtsgeschwindigkeiten, sondern stellt auch einen Vergleich der Kennzahlen in verschiedenen Phasen dar. Ein zentraler Bestandteil ist der statistische Signifikanztest, der berechnet, ob eine Veränderung der Geschwindigkeit – sei es eine Ab- oder Zunahme – statistisch signifikant ist. Dies hilft zu ermitteln, ob es eine wahrscheinliche Ursache für die Geschwindigkeitsänderung gibt. Während des Betriebs wird erwartet, dass die Smiley-Anzeige die Schnellfahrer zum Bremsen anregt. Interessanterweise zeigen sich jedoch auch signifikante Ab- und Zunahmen der Ausfahrtsgeschwindigkeit in den Phasen der Vor- und Nachmessung, was fast die Regel zu sein scheint. Diese Veränderungen sind schwieriger zu erklären, da in diesen Phasen die Anzeige nicht aktiv ist. Eine mögliche Erklärung könnte sein, dass allein die Anwesenheit der Smiley-Messanlage – auch wenn sie nicht aktiv ist – bei den Fahrerinnen und Fahrern eine Geschwindigkeitsreduktion bewirkt.
"""

STAT_TABLE_INFO = """
Beim Vergleich der Ein- und Ausfahrtsgeschwindigkeiten einer Fahrzeug-Durchfahrt werden folgende Verhaltensweisen erwartet bzw. erhofft:

- In der Vormessungsphase sollte die Differenz zwischen Einfahrts- und Ausfahrtsgeschwindigkeit an der Station gering sein, da keine Anzeige vorhanden ist, die die Fahrer zu einer Geschwindigkeitsreduktion anregt. Generell wird erwartet, dass die Geschwindigkeiten in dieser Phase höher sind als in der Betriebsphase, in der durch die Anzeige eine geschwindigkeitsreduzierende Wirkung angenommen wird.
- Während der Betriebsphase wird erwartet, dass die Fahrzeuge ihre Geschwindigkeit an der Messstelle reduzieren, insbesondere wenn ihnen eine Geschwindigkeitsübertretung durch ein 😡-Symbol angezeigt wird.
- In der Nachmessungsphase wird ein "Memory-Effekt" nach Beendigung des Betriebs erhofft. Es wird erwartet, dass die Geschwindigkeiten vor und nach der Durchfahrt zwar wieder ähnlich sind, da keine explizite Mahnung erfolgt, jedoch sollte idealerweise ein Teil der Fahrer aufgrund der Erinnerung an die Smileys der vergangenen Monate ihre Geschwindigkeit freiwillig reduzieren.

Kennzahlen:
Die Überprüfung dieser Erwartungen soll anhand von Grafiken und Kennzahlen erfolgen. Relevant sind hierbei die Differenz der Median-Geschwindigkeiten zwischen Einfahrt und Ausfahrt, welche das allgemeine Verhalten abbildet. Die Differenz der Geschwindigkeiten beim 85-Prozentil veranschaulicht die Veränderung der Geschwindigkeit der schnellsten 15 % der Fahrzeuge. Besonders wichtig ist die Differenz in der Anzahl der Geschwindigkeitsüberschreitungen, da das Ziel der Smiley-Anzeige eine Reduktion dieser Überschreitungen ist. Ein statistisch signifikanter Effekt ist anzunehmen, wenn in der Vormessungsphase der Anteil der Stationen, bei denen die Ausfahrtsgeschwindigkeit niedriger als die Einfahrtsgeschwindigkeit ist, bei etwa 50 % liegt, in der Betriebsphase aber deutlich darüber. Dies ähnelt dem Münzwurf-Prinzip, bei dem das Verhältnis von Kopf zu Zahl bei einer unmanipulierten Münze ebenfalls bei 50 % liegt, bei einer manipulierten Münze jedoch abweicht.
"""

STAT_TEXT = """
**{0}:**

An den selektierten Stationen wurden in der Phase {0} insgesamt {1} Messungen durchgeführt. Bei {2} von {3} Standorten ({4}%) nahm der Median der Geschwindigkeit nach Anzeige des Smileys in der Phase {0} ab. Das 85% Perzentil, also die Geschwindigkeit, die bei 85 Prozent der Fahrzeuge unterschritten wurde, fiel durchschnittlich um {5} km/h nach der Smiley Anzeige. Bei {6} Standorten ({7}%) nahm die Geschwindigkeit nach Anzeige des Smileys ab. Bei {8} Standorten ({9}%) nahm im Betrieb die Anzahl der Geschwindigkeitübertretungen ab.
"""

STAT_COLUMNS_DESCRIPTION = """
| Spalte                         | Beschreibung |
|--------------------------------|--------------|
| id_standort                    | ID des Standorts (siehe auch [data.bs](https://data.bs.ch/explore/dataset/100286)) |
| strname                        | Strassenname |
| hausnr                         | Hausnummer |
| geschwind                      | Höchstgeschwindigkeit an Messort |
| phase                          | Phase (Vormessung, Betrieb, Nachmessung) |
| anz                            | Anzahl Messungen |
| v_einfahrt_median              | Median der Geschwindigkeit vor Smiley-Anzeige in km/h |
| v_einfahrt_percentile_85       | Geschwindigkeit, die von 85% der Fahrzeuge unterschritten wird vor Smiley-Anzeige in km/h |
| v_ausfahrt_median              | Median der Geschwindigkeit nach Smiley-Anzeige in km/h |
| v_ausfahrt_percentile_85       | Geschwindigkeit, die von 85% der Fahrzeuge unterschritten wird nach Smiley-Anzeige in km/h |
| uebertretung_einfahrt_median   | Median der Geschwindigkeitsübertretung vor Smiley-Anzeige (Gemessene Geschwindigkeit - zulässige Geschwindigkeit) |
| uebertretung_ausfahrt_median   | Median der Geschwindigkeitsübertretung nach Smiley-Anzeige (Gemessene Geschwindigkeit - zulässige Geschwindigkeit) |
| ist_uebertretung_einfahrt_sum  | Anzahl Übertretungen vor Smiley-Anzeige |
| ist_uebertretung_ausfahrt_sum  | Anzahl Übertretungen nach Smiley-Anzeige |
| ist_uebertretung_einfahrt_pct  | Prozent Übertretungen vor Smiley-Anzeige |
| ist_uebertretung_ausfahrt_pct  | Prozent Übertretungen nach Smiley-Anzeige |
"""

H0_INTRO = """
Statistische Signifikanztests sind ein beliebtes Instrument, um zu untersuchen, ob Unterschiede zwischen zwei abhängigen Messreihen - in unserem Fall die Geschwindigkeit vor und nach der Durchfahrt an einem Messpunkt - rein zufällig sind oder statistisch signifikant. Dabei kommen Nullhypothesen-Tests zum Einsatz, welche die Annahme überprüfen, dass Unterschiede zwischen den Messreihen zufällig sind. Diese Annahme wird anhand der Daten entweder bestätigt oder widerlegt. Die Nullhypothese wird beibehalten, wenn die Wahrscheinlichkeit für zufällige Unterschiede größer als 5% ist. Liegt diese Wahrscheinlichkeit unter 5%, wird die Nullhypothese verworfen, was auf statistisch signifikante Unterschiede hinweist. Diese Wahrscheinlichkeit wird als p-Wert bezeichnet. Für unsere Analyse wird der [Wilcoxon-Vorzeichen-Rang-Test](https://de.wikipedia.org/wiki/Wilcoxon-Vorzeichen-Rang-Test) verwendet. Aufgrund der Versuchsanordnung ist zu erwarten, dass die Ausfahrtsgeschwindigkeiten signifikant niedriger sind als die Einfahrtsgeschwindigkeiten, da die Fahrer auf die Geschwindigkeitsanzeige reagieren. In der Vormessung und Nachmessung hingegen sind keine signifikanten Unterschiede zu erwarten, da die Fahrer keinen systematischen Grund haben, ihre Geschwindigkeit zu ändern

Die deutlichste Abnahme wird bei Fahrzeugen erwartet, bei welchen bei der Einfahrt ein 😡-Emoticon angezeigt wird, da diese Fahrer durch die Anzeige direkt angesprochen werden, ihre Geschwindigkeit zu reduzieren. Um diese Annahme zu überprüfen, wurde der Signifikanztest gezielt auf ein Subset aller Messungen angewendet, nämlich nur für Durchfahrten, bei denen die Einfahrts- die Höchstgeschwindigkeit überstieg. Es wird erwartet, dass in diesen Fällen während der Betriebsphase bei der Ausfahrt eine signifikant geringere Geschwindigkeit gemessen wird, während in den Vor- und Nachmessungen keine signifikanten Unterschiede festgestellt werden sollten, da hier kein direkter Anreiz zur Geschwindigkeitsreduktion gegeben ist.
"""

H0_RESULT_ALL = """
In der Phase {0} ist der Median der Ausfahrtsgeschwindigkeit ist um {1: .1f} km/h {2} als der Median der Einfahrtsgeschwindigkeit. Der Wilcoxon-Vorzeichen-Rang-Test ergibt einen p-Wert von {3: .3e}. Die Nullhypothese wird {4}{5}, somit {6}.
"""

H0_RESULT_EXC = """
Ein zweiter Signifikanztest wurde durchgeführt mit einer Auswahl der Messungen, bei denen die Einfahrtsgeschwindigkeit die erlaubte Höchstgeschwindigkeit überschritt. Das Mittel der Ausfahrtsgeschwindigkeit ist um {0: .1f} km/h {1} als der Median der Einfahrtsgeschwindigkeit. Die Nullhypothese des Wilcoxon-Vorzeichen-Rang-Test wird {2}, somit {3}.
"""
