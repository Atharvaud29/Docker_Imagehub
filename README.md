## This project show how to work with github actions 

In this project the new workflow is created by using Github Actions (kind of CI/CD Pipeline is implemented). Create an Flask application then we will run unit test cases then build & test in this we will create an Docker Image and then Deploy (CD pipeline) to the Docker Hub. So any one can pull that image and run on their machine.

#Project Goal : 

To create an flask application which can automatically run unit test cases, build and test, deploy to docker hub by using github actions to define the workflow. This can help the developers to use CI/CD pipeline and also to pull the image from docker hub then run on their own machine.

#Workflow of project :

![Screenshot 2025-02-17 175956](https://github.com/user-attachments/assets/e33d212d-6235-4a1d-a1f3-51365a4bd5ea)

#Understanding the implementation :

Libraries needed for project are =

    Flask
    Pytest

Create an Docker file, app.py file, test_app.py file and .gitignore file

In app.py run the simple flask in order to print Hello World!

    from flask import Flask
    app=Flask(__name__)
    @app.route("/")
    def home():
        return "Hello World!"
    if __name__=="__main__":
        app.run(host="0.0.0.0",port=5000)

Then get the response in test_app.py file

    from app import app
    def test_home():
        response=app.test_client().get("/")
        assert response.status_code==200
        assert response.data==b"Hello World!"


Now create an .github floder and in that create the workflows floder and in that create cicd.yml file 

In cicd.yml file write down github action workflow code

    name: CI/CD for Dockerized Flask App
    on:
        push:
            branches: [ main ]
        pull_request:
            branches: [ main ]
    jobs:
        build-and-test:
            runs-on: ubuntu-latest

            steps:
                - name: Checkout code
                  uses: actions/checkout@v3
                - name: Set up Python
                  uses: actions/setup-python@v4
                  with:
                    python-version: '3.9'

                - name: Install dependencies
                  run: |
                    python -m pip install --upgrade pip
                    pip install flask
                    pip install pytest

                - name: Run tests
                  run: |
                    pytest

        build-and-publish:
            needs: build-and-test
            runs-on: ubuntu-latest
            steps:
                - name: Checkout code
                  uses: actions/checkout@v3
                - name: Set up Docker Buildx
                  uses: docker/setup-buildx-action@v2
                - name: Login to Dockerhub
                  uses: docker/login-action@v2
                  with:
                    username: ${{ secrets.DOCKER_USERNAME }}
                    password: ${{ secrets.DOCKER_PASSWORD }}

                - name: Build and push Docker image
                  uses: docker/build-push-action@v4
                  with:
                    context: .
                    file: ./DockerFile
                    push: true
                    tags: ${{ secrets.DOCKER_USERNAME }}/flasktest-app:latest

                - name: Image digest
                  run: echo ${{ steps.build-and-publish.outputs.digest }}

As soon as you commit this in your github repro then github action workflow will run.
This will first run the Build-and-test job then it will run the next Build-and-publish job.

![Screenshot 2025-02-17 185459](https://github.com/user-attachments/assets/d5f69f37-62ea-44e3-a346-28f98a0e7b51)

After successful runnig the workflow, you can see an image is created in your docker hub. 
        
Docker hub image :

![Screenshot 2025-02-17 183610](https://github.com/user-attachments/assets/a1abfe8f-1d71-42c1-8822-67cc0b52390c)

In this you can see all the values and paramenters of your experiment

Now you can deploy any flask application on docker hub by completely automatic the workflow using github actions.


