# # Use an official Python runtime as a parent image
FROM python:3.11.1

# # Set the working directory to /app
WORKDIR /app

# # Copy the current directory contents into the container at /app
COPY employee_server.py /app/
COPY employee_form.html /app/
COPY employee_data.csv /app/

# # Make port 80 available to the world outside this container
EXPOSE 8080

# # Define environment variable
ENV NAME World

# # Run app.py when the container launches
CMD ["python", "employee_server.py"]

-------------------------------------------------------------------------------------------------------------------

#The following docker code is for the new image for the inventory page

FROM python:3.11.1

WORKDIR /app

COPY inventory.py /app/

EXPOSE 8000

ENV NAME world

CMD [ "python","inventory.py" ]
