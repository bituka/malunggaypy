FROM codenvy/python27
RUN wget -qO- "https://storage.googleapis.com/appengine-sdks/deprecated/1914/google_appengine_1.9.14.zip" -O /tmp/gae-sdk.zip && \
    unzip -qq /tmp/gae-sdk.zip -d /home/user && \
    rm /tmp/gae-sdk.zip
EXPOSE 8080
ENV CODENVY_APP_PORT_8080_HTTP 8080
RUN mkdir /home/user/app
ADD $app$ /home/user/app/
CMD /home/user/google_appengine/dev_appserver.py 2>&1 --host 0.0.0.0 --skip_sdk_update_check true /home/user/app

#APP ENGINE UPLOAD
# google_appengine/appcfg.py update app


#FROM codenvy/python27

#RUN wget -qO- "https://storage.googleapis.com/appengine-sdks/deprecated/1914/google_appengine_1.9.14.zip" -O /tmp/gae-sdk.zip && \
#    unzip -qq /tmp/gae-sdk.zip -d /home/user && \
#    rm /tmp/gae-sdk.zip

#EXPOSE 8080
#ENV CODENVY_APP_PORT_8080_HTTP 8080

#RUN mkdir /home/user/application

#ADD $app$/ /home/user/application

#RUN sudo virtualenv /env

#CMD sudo chmod a+rw -R /home/user/application/ && \
#    umask 0 && \
#    /env/bin/python /home/user/google_appengine/dev_appserver.py --host 0.0.0.0 --skip_sdk_update_check true /home/user/application 
#    
#    
