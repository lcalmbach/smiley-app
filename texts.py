INFO = """# Smiley-App
Smiley-Geschwindigkeitsanzeigen sind ein innovatives Instrument zur Erhöhung der Verkehrssicherheit. Diese Anzeigen wechseln zwischen der angezeigten Geschwindigkeit und einem Smiley-Symbol, das entweder Lob (für Einhalten des Tempolimits) oder Tadel (bei Überschreitung) ausdrückt. Dies geschieht auf eine nicht-bestrafende, freundliche Art und Weise. Seit Anfang Februar 2023 sind 20 solcher neuen Geräte im Einsatz. Sie zeichnen sich durch ihre flexible Einsetzbarkeit und batteriebetriebene Stromversorgung aus, wodurch sie an verschiedenen Orten aufgestellt werden können. Bei der Auswahl der Standorte, insgesamt 75 an der Zahl, lag der Fokus besonders auf sensiblen Bereichen wie Kindergärten, Schulen und Altersheimen. Diese Standorte wurden nach einer umfassenden Evaluation unter Einbeziehung von Fachleuten aus der Kantonsverwaltung und Rückmeldungen aus der Bevölkerung festgelegt. Die 20 Smiley-Geschwindigkeitsanzeigen rotieren zwischen den 75 Standorten und werden an jedem Ort für etwa fünf Monate aufgestellt. Das besondere an ihrem Einsatz: Zunächst messen sie für einen Monat die Geschwindigkeit, ohne dass die Anzeige aktiviert ist. Ab März 2023 sind die Anzeigen für drei Monate eingeschaltet, um dann im letzten Monat erneut ohne aktive Anzeige zu messen. Dieses Muster wird bei zukünftigen Einsätzen beibehalten, um die Effektivität der Anzeigen zu bewerten.

Die während dieser Zeit gesammelten Daten dienen als wichtige Grundlage für Massnahmen zur Erhöhung der Verkehrssicherheit. [Mehr Informationen finden Sie in der Medienmitteilung des JSD des Kantons Basel-Stadt.](https://www.jsd.bs.ch/nm/2023-start-des-betriebs-der-neuen-praeventiven-smiley-geschwindigkeitsanzeigen---ab-maerz-2023-aktiv-jsd.html)

**Datenaufbereitung und Ausreisser-Werte**

Die Rohdaten, die von diesen Geräten gesammelt wurden, sind öffentlich zugänglich auf dem [OGD-Portal](https://data.bs.ch/explore/dataset/100268) des Kantons Basel-Stadt. Bei der Durchsicht dieser Daten fällt auf, dass einige unrealistisch hohe Geschwindigkeiten, wie z.B. 231 km/h in einer 20 km/h-Zone, gemessen wurden. Solche Werte können vor allem bei der graphischen Darstellung stören. Um solche Ausreisser zu bereinigen, wurden statistische Methoden angewendet: Für jede Messstation wurde der Z-Wert, ein Mass für die Abweichung vom Durchschnitt, berechnet. Alle Messungen, deren Z-Wert grösser als 3 oder kleiner als -3 war, wurden aus den Daten entfernt. Diese Methode gewährleistet, dass nur realistische Werte in der Analyse berücksichtigt werden. Dadurch wurden etwa 0.3% der Daten als Ausreisser identifiziert und entfernt. Es ist wichtig zu verstehen, dass ein Z-Wert von -3 oder 3 weit ausserhalb des normalen Bereichs liegt – das entspricht den extremsten 0,3% aller Werte. Diese statistische Filterung hilft dabei, die Daten realitätsgetreu und aussagekräftig zu halten.

Diese Art der Datenbereinigung ist ein wichtiger Schritt, um sicherzustellen, dass die Analysen und daraus abgeleiteten Massnahmen zur Verkehrssicherheit auf zuverlässigen und repräsentativen Daten basieren.
"""

STAT_TEXT = """Beim Vergleich von Ein/Ausfahrts Geschwindigkeiten wird erwartet, dass die Geschwindigkeit nach Anzeige des Smileys abnimmt, und zwar besonders bei Fahrzeugen, bei denen die Ampel eine Übertretung anzeigt. Bei den Vormessungen sollte hingegen keine signifikater Unterschied feststellbar sein, das heisst, die Geschwindigkeit nimmt bei je 50% der Fahrzeuge zu oder ab. Je mehr sich im Betrieb das Verhältnis von Geschwindikeitsabnahmen zu Zunahmen von 50% entfernt, deste statistisch wahrscheinlicher ist es, dass die Smiley-Anzeige für die Abnahme verantwortlich ist. Es ist auch zu hoffen, dass die Smiley Anzeige bei zu schnell fahrenden Fahrzugen effektiver ist, als bei korrekt fahrenden, bei welchen eine Geschwindigkeitsreduktion nicht erforderlich ist. Diese Annahmen werden nun mit den Daten in folgendem Abschnitt überprüft. Bei der Vormessung ist zu erwarten dass die Abnahme Von GEschwindigkeit zwischen Vor und Nach-Smiley Messung bei zirka 50% liegt, also rein zufällig sind, da noch keine Anzeige erfolgt. Bei der Nachmessung ist zu erwarten, dass die Geschwindigkeit gegenüber dem Betrieb wieder zunimmt, da di eAnzeige ausgeschaltet ist, jedoch ist zu hoffen, dass sich die Fahrenden an die Anzeige erinnern und daher trotz ausgeschalteter Anzeige langsamer fahren. Diese Annahmen werden nun mit den Daten in folgendem Abschnitt überprüft.

**Vormessung:**

**Betrieb:**

An den selektierten Stationen wurden insgesamt {0} Messungen durchgeführt. Bei {1} von {2} Standorten ({3}%) nahm der Median der Geschwindigkeit nach Anzeige des Smileys im Betrieb ab. Das 85% Perzentil, also die Geschwindigkeit, die bei 85 Prozent der Fahrzeuge unterschritten wurde, fiel durchschnittlich um {4} km/h nach der Smiley Anzeige. Bei {5} Standorten ({6}%) nahm die Geschwindigkeit nach Anzeige des Smileys ab. Bei {7} Standorten ({8}%) nahm im Betrieb die Anzahl der Geschwindigkeitübertretungen ab.

**Nachmessung**:

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
