FROM nginx:1.18
RUN apt-get update  && apt-get -y install curl
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY metals.xml /usr/share/nginx/html
HEALTHCHECK CMD curl -f http://localhost:80/ || exit 1
EXPOSE 80
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
