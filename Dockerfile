FROM bengabp/sandbox:base

EXPOSE 3000 5900 6080

WORKDIR /app
COPY . .

ENV DISPLAY=:99

CMD ["sh", "./entrypoint.sh"]
