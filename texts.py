INFO = """# Smiley-App
Smiley-Geschwindigkeitsanzeigen sind ein innovatives Instrument zur Erhöhung der Verkehrssicherheit. Diese Anzeigen wechseln zwischen der angezeigten Geschwindigkeit und einem Smiley-Symbol, das entweder Lob (für Einhalten des Tempolimits) oder Tadel (bei Überschreitung) ausdrückt. Dies geschieht auf eine nicht-bestrafende, freundliche Art und Weise. Seit Anfang Februar 2023 sind 20 solcher neuen Geräte im Einsatz. Sie zeichnen sich durch ihre flexible Einsetzbarkeit und batteriebetriebene Stromversorgung aus, wodurch sie an verschiedenen Orten aufgestellt werden können. Bei der Auswahl der Standorte, insgesamt 75 an der Zahl, lag der Fokus besonders auf sensiblen Bereichen wie Kindergärten, Schulen und Altersheimen. Diese Standorte wurden nach einer umfassenden Evaluation unter Einbeziehung von Fachleuten aus der Kantonsverwaltung und Rückmeldungen aus der Bevölkerung festgelegt. Die 20 Smiley-Geschwindigkeitsanzeigen rotieren zwischen den 75 Standorten und werden an jedem Ort für etwa fünf Monate aufgestellt. Das besondere an ihrem Einsatz: Zunächst messen sie für einen Monat die Geschwindigkeit, ohne dass die Anzeige aktiviert ist. Ab März 2023 sind die Anzeigen für drei Monate eingeschaltet, um dann im letzten Monat erneut ohne aktive Anzeige zu messen. Dieses Muster wird bei zukünftigen Einsätzen beibehalten, um die Effektivität der Anzeigen zu bewerten.

Die während dieser Zeit gesammelten Daten dienen als wichtige Grundlage für Massnahmen zur Erhöhung der Verkehrssicherheit. [Mehr Informationen finden Sie in der Medienmitteilung des JSD des Kantons Basel-Stadt.](https://www.jsd.bs.ch/nm/2023-start-des-betriebs-der-neuen-praeventiven-smiley-geschwindigkeitsanzeigen---ab-maerz-2023-aktiv-jsd.html)

**Datenaufbereitung und Ausreisser-Werte**

Die Rohdaten, die von diesen Geräten gesammelt wurden, sind öffentlich zugänglich auf dem [OGD-Portal](https://data.bs.ch/explore/dataset/100268) des Kantons Basel-Stadt. Bei der Durchsicht dieser Daten fällt auf, dass einige unrealistisch hohe Geschwindigkeiten, wie z.B. 231 km/h in einer 20 km/h-Zone, gemessen wurden. Solche Werte können vor allem bei der graphischen Darstellung stören. Um solche Ausreisser zu bereinigen, wurden statistische Methoden angewendet: Für jede Messstation wurde der Z-Wert, ein Mass für die Abweichung vom Durchschnitt, berechnet. Alle Messungen, deren Z-Wert grösser als 3 oder kleiner als -3 war, wurden aus den Daten entfernt. Diese Methode gewährleistet, dass nur realistische Werte in der Analyse berücksichtigt werden. Dadurch wurden etwa 0.3% der Daten als Ausreisser identifiziert und entfernt. Es ist wichtig zu verstehen, dass ein Z-Wert von -3 oder 3 weit ausserhalb des normalen Bereichs liegt – das entspricht den extremsten 0,3% aller Werte. Diese statistische Filterung hilft dabei, die Daten realitätsgetreu und aussagekräftig zu halten.

**Analyse der Einzelmessungen**
Der Datensatz von 2023 besteht aus über 6 Mio Einzelmessungen an 35 Standorten. Diese grosse Datenmenge bedeutet eine Herausforderung für eine aussagekräftige Analyse. Die grafischen und numerischen Methoden der applikation smiley-app macht folgende Annahmen und versucht sie mit den Daten zu überprüfen:
- In der Vormessung und Nachmessung unterscheidet sich die Geschwindigkeit der Fahrzeuge bei der Einfahrt und Ausfahrt nicht wesentlich, da die Anzeige nicht aktiv ist.
- Im Betrieb wird die Geschwindigkeit der Fahrzeuge bei der Einfahrt und Ausfahrt unterschiedlich sein, da die Anzeige aktiv ist, und zu schnelle Fahrende ihr Tempo nach einer 😡 Anzeige reduzieren. Es wird erwartet, dass dieser Effekt vor allem bei Fahrzeugen auftritt, schnell fahren, weshalb die 85-Perzentil Geschwindigkeit stärker reduziert wird als der Median. 
- Die Geschwindigkeiten sind in der Vormessung am höchsten und Zu und Abnahme der Geschwindigkeit am Smiley Standort sind etwas zufällig, da die Anzeige ja noch nicht aktiv ist und es für die Fahrenden keinen Anlass gibt, die Geschwindigkeit am Standort zu reduzieren. Im Betrieb wird die Geschwindigkeit von Einfahrt zu Ausfahrt reduziert und zwar am stärksten bei hohen Geschwindigkeiten. Da man das Smiley von weitem sieht, ist bereits ein gewisser reduziernder Effekt bei der Einfahrt zu erwarten. In der Nachmessung wird erwartet, dass ein Teil der Fahrenden, welche die Strecke regelmässig befahren, ihr Tempo aus Gewohnheit der letzten 3 Monate reduzieren und es ist eine Geschwindigkeitesabnahme gegenüber der Vormessung zu erwarten, jedoch nicht so stark wie im Betrieb. Zudem sollte die Einfahrts und Ausfahrtsgeschwindigkeit wieder ähnlich sein, da die Anzeige nicht mehr aktiv ist.

**Statistiken**
Die Kennzahlen, die uns bei der Frage der obigen Antworten helfen sind:
- Median der Differenz von Ausfahrts- und Einfahrts-Geschwindigkeit:
- 85-Perzentil der Differenz von Ausfahrts- und Einfahrts-Geschwindigkeit: Geschwindigkeit der schnellsten 15% der Fahrzeuge
- Anzahl Übertretungen
- Median der Geschwindigkeitsübertretung
- 85-Perzentil der Geschwindigkeitsübertretung

"""

STAT_TABLE_INFO = """
Beim Vergleich von Ein- und Ausfahrtsgeschwindigkeiten wird folgendes Verhalten erwartet:

- In der Vormessungsphase sollte sich die Einfahrts- und Ausfahrtsgeschwindigkeit an der Station nicht ändern, da noch keine Anzeige vorhanden ist, die die Fahrer zum Abbremsen motiviert. Generell sollten die Geschwindigkeiten höher sein als in der Betriebsphase, in der eine geschwindigkeitsreduzierende Wirkung durch die Anzeige erwartet wird, und als in der Nachmessungsphase, in der ein Nachwirken der Betriebsphase erhofft wird.
- In der Betriebsphase wird erwartet, dass die Fahrzeuge ihre Geschwindigkeit bei der Durchfahrt an der Messstelle reduzieren, insbesondere wenn ihnen eine Geschwindigkeitsübertretung angezeigt wird. Die Ausfahrtsgeschwindigkeiten sollten niedriger sein als bei der Vormessung.
- In der Nachmessungsphase wird ein "Memory-Effekt" nach dem Betrieb erhofft. Die Geschwindigkeiten vor und nach der Durchfahrt sollten wieder sehr ähnlich wie bei der Vormessung sein, aber idealerweise niedriger als bei der Vormessung.

Kennzahlen:

Als Kennzahlen dienen einerseits die Differenz der Median-Geschwindigkeit zwischen Einfahrt und Ausfahrt, die das allgemeine Verhalten beschreibt. Die Differenz der Geschwindigkeiten beim 85-Prozentil zeigt die Veränderung der Geschwindigkeit der schnellsten 15 % der Fahrzeuge. Die Differenz der Anzahl der Überschreitungen ist der wichtigste Parameter im Betrieb: Die Smiley-Anzeige soll die Anzahl der Überschreitungen reduzieren.

Ein statistischer Effekt ist wahrscheinlich, wenn bei der Vormessung der Anteil der Stationen, bei denen die Ausfahrtsgeschwindigkeit < Einfahrtsgeschwindigkeit liegt, bei 50 % liegt, im Betrieb aber wesentlich über 50 % liegt. Ähnlich wie beim Münzwurf, wo bei einer normalen Münze das Verhältnis Kopf/Zahl bei 50 % liegt, weicht das Verhältnis bei einer manipulierten Münze ab.
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
