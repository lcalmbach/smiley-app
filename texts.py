INFO = """# Smiley-App
Smiley-Geschwindigkeitsanzeigen sind ein innovatives Instrument zur Erhöhung der Verkehrssicherheit. Diese Anzeigen wechseln zwischen der angezeigten Geschwindigkeit und einem Smiley-Symbol, das entweder Lob (für Einhalten des Tempolimits) oder Tadel (bei Überschreitung) ausdrückt. Dies geschieht auf eine nicht-bestrafende, freundliche Art und Weise. Seit Anfang Februar 2023 sind 20 solcher neuen Geräte im Einsatz. Sie zeichnen sich durch ihre flexible Einsetzbarkeit und batteriebetriebene Stromversorgung aus, wodurch sie an verschiedenen Orten aufgestellt werden können. Bei der Auswahl der Standorte, insgesamt 75 an der Zahl, lag der Fokus besonders auf sensiblen Bereichen wie Kindergärten, Schulen und Altersheimen. Diese Standorte wurden nach einer umfassenden Evaluation unter Einbeziehung von Fachleuten aus der Kantonsverwaltung und Rückmeldungen aus der Bevölkerung festgelegt. Die 20 Smiley-Geschwindigkeitsanzeigen rotieren zwischen den 75 Standorten und werden an jedem Ort für etwa fünf Monate aufgestellt. Das besondere an ihrem Einsatz: Zunächst messen sie für einen Monat die Geschwindigkeit, ohne dass die Anzeige aktiviert ist. Ab März 2023 sind die Anzeigen für drei Monate eingeschaltet, um dann im letzten Monat erneut ohne aktive Anzeige zu messen. Dieses Muster wird bei zukünftigen Einsätzen beibehalten, um die Effektivität der Anzeigen zu bewerten.

Die während dieser Zeit gesammelten Daten dienen als wichtige Grundlage für Massnahmen zur Erhöhung der Verkehrssicherheit. [Mehr Informationen finden Sie in der Medienmitteilung des JSD des Kantons Basel-Stadt.](https://www.jsd.bs.ch/nm/2023-start-des-betriebs-der-neuen-praeventiven-smiley-geschwindigkeitsanzeigen---ab-maerz-2023-aktiv-jsd.html)

**Datenaufbereitung und Ausreisser-Werte**

Die Rohdaten, die von diesen Geräten gesammelt wurden, sind öffentlich zugänglich auf dem [OGD-Portal](https://data.bs.ch/explore/dataset/100268) des Kantons Basel-Stadt. Bei der Durchsicht dieser Daten fällt auf, dass einige unrealistisch hohe Geschwindigkeiten, wie z.B. 231 km/h in einer 20 km/h-Zone, gemessen wurden. Solche Werte können vor allem bei der graphischen Darstellung stören. Um solche Ausreisser zu bereinigen, wurden statistische Methoden angewendet: Für jede Messstation wurde der Z-Wert, ein Mass für die Abweichung vom Durchschnitt, berechnet. Alle Messungen, deren Z-Wert grösser als 3 oder kleiner als -3 war, wurden aus den Daten entfernt. Diese Methode gewährleistet, dass nur realistische Werte in der Analyse berücksichtigt werden. Dadurch wurden etwa 0.3% der Daten als Ausreisser identifiziert und entfernt. Es ist wichtig zu verstehen, dass ein Z-Wert von -3 oder 3 weit ausserhalb des normalen Bereichs liegt – das entspricht den extremsten 0,3% aller Werte. Diese statistische Filterung hilft dabei, die Daten realitätsgetreu und aussagekräftig zu halten.

Diese Art der Datenbereinigung ist ein wichtiger Schritt, um sicherzustellen, dass die Analysen und daraus abgeleiteten Massnahmen zur Verkehrssicherheit auf zuverlässigen und repräsentativen Daten basieren.
"""

STAT_TABLE_INFO = """
Beim Vergleich von Ein/Ausfahrts Geschwindigkeiten Folgendes erwartet: 

- Bei der Vormessungsphase sollte sich Einfahrts und Ausfahrtsgeschwindikeit an der STation nicht ändern, da es ja noch keine Anzeige gibt. Generell sollten die GEschwindikeiten höher sein als im Betrieb, wo ein durch die Anzeige reduzierende wirkung erwartet wird und als in der NAchmessung, wo eine Nachworking der Betreibsphase erhofft wird. 
- In der Phase Betrieb wird erwartet, dass die Fahrzeuge ihre Geschwindigkeit bei der Durchfahrt an der Messstelle reduzieren, insbesondere, wenn ihnen eine Geschwindigkeitesübertretung aangezeigt wird. die Ausfahrtsgeschwindigkeiten sollte tiefer als bei der Vormessung sein.
- Bei der Phase Nachmessung wird ein Memory Effekt nach dem Betrieb erhofft. die Geschwindig vor und nach der Duchfahrt sind wieder sehr ähnlich wie bei der Vormessung, aber im Idealfall tiefer als bei der Vormessung.

Kennzahlen:

Als Kennzahlen wird einerseits die Differenz der Median-Geschwindigkeit zwischen Einfahrt und Ausfahrt. Sie beschreibt das allgemeine Verhalten. die Differenz der 85-PErzentil-Geschwindigkeiten zeigt die Veränderung der Geschwindigkeit der schnellsten 15% der Fahrzeuge. Die Differenz der Anzahl Überschreitungen ist der wichtigste Parameter im Betreib: die Smiley-Anzeige soll die Anzahl Überschreitungen reduzieren.

Ein statistischer Effekt ist dann wahrscheinlich, wenn bei der Vormessung der Anteil der Stationen bei der Ausfahrt < Einfahrtsgeschwindigkeit bei 50%-, im Betrieb aber wesentlich über 50% liegt. Ändlich wie beim Münzwurf, wo bei einer normalen Münze das Verhältnis Kopf/Zahl bei 50% leigt, bei einer getürkten Münze das Verhältnis abweicht.
"""

STAT_TEXT = """
**{0}:**

An den selektierten Stationen wurden in der Phase {0} insgesamt {1} Messungen durchgeführt. Bei {2} von {3} Standorten ({4}%) nahm der Median der Geschwindigkeit nach Anzeige des Smileys im Betrieb ab. Das 85% Perzentil, also die Geschwindigkeit, die bei 85 Prozent der Fahrzeuge unterschritten wurde, fiel durchschnittlich um {5} km/h nach der Smiley Anzeige. Bei {6} Standorten ({7}%) nahm die Geschwindigkeit nach Anzeige des Smileys ab. Bei {8} Standorten ({9}%) nahm im Betrieb die Anzahl der Geschwindigkeitübertretungen ab.
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
