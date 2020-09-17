# Task 2 Answers
* what are the median and variance observed from the temperature data (at least 100 values)  [3 points]
* The median and variance of the temperatures are:
lab 1: 20.987, 2.207
class 1: 26.947, 136.274
Office: 23.004, 51.040
Global: 23.00, 68.63
* what are the median and variance observed from the occupancy data (at least 100 values)  [3 points]
* The median and variance of the occupancy are:
lab1       5.0, 4.46
class1    19.0, 19.73
office     2.0, 2.0
Global: 5.0, 63.83
* plot the probability distribution function for each sensor type? [6 points]
* What is the mean and variance of the *time interval* of the sensor readings? Please plot its probability distribution function. Does it mimic a well-known distribution for connection intervals in large systems? [8 points]
*The mean and variance of the time in between arrivals is 0.928 and 0.8439
In stochastic processes, arrivals are often modeled as poisson distributions, yielding exponential waiting times between arrivals
Assuming a lambda of 1.078, an exponential distribution would have a mean of 0.927 and a variance of 0.860, which is the case here. There is some difference due to rounding in calculations
From the source code, the distribution is generated from an erlang waiting time with k = 1, which simplifies to exponential as expected

# Task 3 Answers
* implement an algorithm that detects anomalies in **temperature** sensor data
* Does a persistent change in temperature always indicate a failed sensor?
* As a practical measure in the above example, we used a 5-95 filter to deal with outliers, but given that the cauchy distribution used is very similar to a normal distribution in this case, we can also try to detect them by filtering by two standard distributions
* Even with a driven change in temperature, two standard deviations will still throw some false failures, but should be cautious enough to catch failures.
* A persistent change would not indicate a failed sensor in a real system, because these sensors are simulated on the back end by a defined distribution, it likely would. Temperature changes for all kinds of reasons, daily temperature cycles, occupences, etc that would drive persistent changes.
* What are possible bounds on temperature for each room type?
* The temperature appears to be normally distributed, so bounds were defined using 2*sqrt(variance) for each sensor. Technically, there aren't any hard bounds on what the sensor could read.

# Sensor simulation miniproject Report
The following analysis examines and describes the behavior of a simulated IoT network consisting of occupant, temperature and co2 sensors.
	
	The simulated network captures many of the variables that a building manager would desire to know. Occupancy can relate to regulations on ventilation, temperature and co2 can be a diagnostic tool for such ventilation, and co2 also presents its own unique dangers. The simulation also reflects some stochastic elements found in the real world, such as in the distribution of arrival times for connections.  Often random arrivals of information can be modeled by a Poisson distribution, which would yield the exponential waiting time behavior observed. Some elements of the simulated sensors are not reflective of actual behavior though, specifically in how the variables themselves are determined. They are modeled as being drawn from a distribution independently of all other points drawn from that distribution. In reality, they would be more similar to something like a random walk. Instead of being modeled by something like X[n] = normal(mean,sigma), they should be modeled as something closer to X[n] = X[n-1] + normal(0,sigma) with X[0] = mean, or with a more suitably defined walk. Our analysis does not capture the complexity here, as both of these definitions should yield the same time invariant analysis, in that when the mean,median, etc. of either set of data points is taken, the final result should be a normal distribution about some mean. For a much more complex analysis, that would involve data collected over hours, that random walk could also be expanded with some general day trends. For example X[n] = sin(2 * pi * n/( 2* # of time units in a day)) + normal(0, sigma) would generate a noisy curve that would peak in midday. That forcing function can be redesigned to reflect whatever trends are assumed, but would create trends over long time scales.

	A building manager though would be concerned with the time varying analysis, or the actual behavior of the time series. As an example, a room having a temperature of: 21C, 30C, then 17C is markedly different behavior from a series: 17C, 21C, 30C, and the energy consumed by and performance of the ventilation system is completely different in the two scenarios. Our analysis would not find any difference between them, as they would have the same mean and distribution taken as a set. Modeling as a random walk would not change the results of our analysis, but would provide information for other analyses of the same data set. It could also decrease some slightly absurd results such as sensors reading occupancies changing from 17 to 26 to 21 people in a room within a second. 

	One of the flaws in this programming also is that the structure of the program selects which sensor has new data through a random choice, and then generates the new data for that sensor. This algorithm makes it extremely likely that each time a sensor communicates; its measurements will all be different from previous reports. This is not really reflective of behavior though, as each of the variables measured should be able to operate on its own distinct timescale for change. To solve this, expand the decision tree. Once a sensor has been selected at random, generate another random choice for each variable, where in one state the variable retains its previous value, and in the other state the variable takes on the next generated value.
	
	When the sensors should communicate is mostly a question of reliability of environment, reliability of measurement. If the sensors are for environments with predictable movement, such as a school, then a fixed measuring schedule is adequate. In a typical high-school, even though the co2, temperature and occupancy of a classroom is not known, when those variables are likely to start changing is due to the schedule of the institution. In a highly unpredictable environment, ad hoc reporting might be better. If one is attempting to measure these variables for a subway station, where occupancy is driven by a great number of unknown factors on unknown timescales, reporting on a fixed schedule might miss changes. It also does depend on sensor reliability, as sensors do experience wear and it might be beneficial to limit their cycles. If the sensors are highly noisy, then they might also reach out to the server far too frequently, attempting to report seemingly new data, that actually just reflects noisy and minute changes. 
	
	Overall, this framework provides a good test of a possible sensor network, but the algorithms used to generate the sensor data, with some increased complexity could provide more practice in modeling the behavior of a building.
