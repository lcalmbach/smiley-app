INFO = """# Smiley-App
Smiley-Geschwindigkeitsanzeigen sind ein innovatives Instrument zur Erhöhung der Verkehrssicherheit. Diese Anzeigen wechseln zwischen der angezeigten Geschwindigkeit und einem Smiley-Symbol, das entweder Lob (😃für Einhalten des Tempolimits) oder Tadel (😡 bei Überschreitung) ausdrückt. Dies geschieht auf eine nicht-bestrafende, freundliche Art und Weise. Seit Anfang Februar 2023 sind 20 solcher neuen Geräte im Einsatz. Sie zeichnen sich durch ihre flexible Einsetzbarkeit und batteriebetriebene Stromversorgung aus, wodurch sie an verschiedenen Orten aufgestellt werden können. Bei der Auswahl der Standorte, insgesamt 75 an der Zahl, lag der Fokus besonders auf sensiblen Bereichen wie Kindergärten, Schulen und Altersheimen. Diese Standorte wurden nach einer umfassenden Evaluation unter Einbeziehung von Fachleuten aus der Kantonsverwaltung und Rückmeldungen aus der Bevölkerung festgelegt. 

Die 20 Smiley-Geschwindigkeitsanzeigen rotieren zwischen den 75 Standorten und werden an jedem Ort für etwa fünf Monate aufgestellt. Es wird jeweils die Geschwindigkeit vor dem Smiley Standort und nach dem Smiley Standort gemessen. Eine Messperiode setzt sich aus einer Phase Vormessung (1 Monat), Betrieb(3 Monate) Nachmesssung (1 Monat) zusammen. Während Vor- und Nachmessung werden die Geschwindigkeiten gemessen ohne Anzeige, in der Phase Betrieb wird den Fahrenden die Einfahrtsgeschwindkit mit Smiley angezeigt. Mit diesen Messungen lässt sich die Effektivität der Smiley Anzeige während dem Betrieb, aber auch etwaige Nachwirkung auf das Fahrverhalten mit der Nachmessung analysieren. [Mehr Informationen finden Sie in der Medienmitteilung des JSD des Kantons Basel-Stadt.](https://www.jsd.bs.ch/nm/2023-start-des-betriebs-der-neuen-praeventiven-smiley-geschwindigkeitsanzeigen---ab-maerz-2023-aktiv-jsd.html)

**Datenaufbereitung und Ausreisser-Werte**

Die Rohdaten, die von diesen Geräten gesammelt wurden, sind öffentlich zugänglich auf dem [OGD-Portal](https://data.bs.ch/explore/dataset/100268) des Kantons Basel-Stadt. Bei der Durchsicht dieser Daten fällt auf, dass einige unrealistisch hohe Geschwindigkeiten, wie z.B. 231 km/h in einer 20 km/h-Zone, gemessen wurden. Solche extreme Werte werden als Ausreisser bezeichnet. Sie stören vor allem bei der graphischen Darstellung. 

**Analyse der Einzelmessungen**
Der Datensatz von 2023 besteht aus über 6 Mio Einzelmessungen an 35 Standorten. Diese grosse Datenmenge bedeutet eine Herausforderung für eine aussagekräftige Analyse. Die grafischen und numerischen Methoden der applikation smiley-app macht folgende Annahmen und versucht sie mit den Daten zu überprüfen:
- In der Vormessung und Nachmessung unterscheidet sich die Geschwindigkeit der Fahrzeuge bei der Einfahrt und Ausfahrt nicht wesentlich, da die Anzeige nicht aktiv ist.
- Im Betrieb wird die Geschwindigkeit der Fahrzeuge bei der Einfahrt und Ausfahrt unterschiedlich sein, da die Anzeige aktiv ist, und zu schnelle Fahrende ihr Tempo nach einer 😡 Anzeige reduzieren. Es wird erwartet, dass dieser Effekt vor allem bei Fahrzeugen auftritt, schnell fahren, weshalb die 85-Perzentil Geschwindigkeit stärker reduziert wird als der Median. 
- Die Geschwindigkeiten sind in der Vormessung am höchsten und Zu und Abnahme der Geschwindigkeit am Smiley Standort sind etwas zufällig, da die Anzeige ja noch nicht aktiv ist und es für die Fahrenden keinen Anlass gibt, die Geschwindigkeit am Standort zu reduzieren. Im Betrieb wird die Geschwindigkeit von Einfahrt zu Ausfahrt reduziert und zwar am stärksten bei hohen Geschwindigkeiten. Da man das Smiley von weitem sieht, ist bereits ein gewisser reduziernder Effekt bei der Einfahrt zu erwarten. In der Nachmessung wird erwartet, dass ein Teil der Fahrenden, welche die Strecke regelmässig befahren, ihr Tempo aus Gewohnheit der letzten 3 Monate reduzieren und es ist eine Geschwindigkeitesabnahme gegenüber der Vormessung zu erwarten, jedoch nicht so stark wie im Betrieb. Zudem sollte die Einfahrts und Ausfahrtsgeschwindigkeit wieder ähnlich sein, da die Anzeige nicht mehr aktiv ist.

**Statistiken**

Die Kennzahlen, die uns bei der Frage der obigen Antworten helfen sind:
- Median der Differenz von Ausfahrts- und Einfahrts-Geschwindigkeit:
- 85-Perzentil der Differenz von Ausfahrts- und Einfahrts-Geschwindigkeit: Geschwindigkeit der schnellsten 15% der Fahrzeuge
- Anzahl Geschwindigkeitsübertretungen
- Median der Geschwindigkeitsübertretungen
- 85-Perzentil der Geschwindigkeitsübertretungen

**Analysemöglicheiten**

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
H0_RESULT = """
Der Median der Ausfahrtsgeschwindigkeit ist um {0: .1f} km/h {1} als der Median der Einfahrtsgeschwindigkeit. Ein [Wilcoxon-Vorzeichen-Rang-Test](https://de.wikipedia.org/wiki/Wilcoxon-Vorzeichen-Rang-Test) mit Alpha = 0.05 wurde durchgeführt, um die statistische Relevanz der Geschwindigkeitsunterschiede zu überprüfen. Die Nullhypothese (Annahme: kein Unterschied) wird {2}, somit {3}."""