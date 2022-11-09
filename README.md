# Finalysis Task

## Goal
To Determine if Apple stock is correlated with the location of the International Space station (ISS).

RESTful server that calculates a correlation matrix between apple stock and ISS.

## Information Given
 - Current Location of ISS is found [Here](http://open-notify.org/Open-Notify-API/ISS-Location-Now/)

 - Intraday Historical Data can be found [Here](https://firstratedata.com/free-intraday-data)  
 **Please Note:** The data available was only for 2019, for convenience, I have replaced the year to 2022 for the 2019 data. But the code would work just fine for current data as well.

 - I have used a different source of ISS Location data because the mentioned website simply returned the current location. The method I am using is fetching the location at a time and then calculating the position at different times based on the degrees the ISS would travel.
 Reference Link [here](https://beebotte.com/tutorials/iss_realtime_position).

## Problem Statement

On request, the application should deliver a correlation matrix for a 5 day period that ends on the last market date closest to the date requested.  
*For example, if a request is made on Sunday, the last market date is Friday.*  
**Output should default to CSV with an optional parameter for HTML.**

## Instructions for execution
Requirements:  
 - Packages: pandas, flask_restful
   You can Install these packages using pip by the following commands:
   - `pip install pandas`
   - `pip install flask_restful`
 - Keep the `AAPL_FirstRateDatacom1.txt` data file in the same folder as the codes.
Execution:
 - The file to be executed is `server_file.py`.  
 *Please Note:* The code `finalysis_task.py` works on the data and calculates the correlation and needs to be in the same folder as the `server_file.py`.

   Navigate to the folder where the files are present and use the following command in command prompt to execute the file:  
   `python server_file.py`
 - This will run a localhost server hosting the functionality.
 - You can then go to any web browser and enter the following URL making your changes:  
 `http://127.0.0.1:5000/{date}/{output type}`  
 where -  
 `{date}` is the last date of the 5 day data that you want.  
 `{output type}` - OPTIONAL. If you would want an output in HTML simply mention `html`. Else, Any other input type might return a csv file with the matrix.  
 *Example:*  
 `http://127.0.0.1:5000/2022-09-09/`  
 `http://127.0.0.1:5000/2022-09-09/html`  
  In case of a *csv* as output, a file shall be downloaded.  
  In case of *html*, the webpage shall reflect the matrix.