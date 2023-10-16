FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build

# copy project files 
WORKDIR Application/src
ADD . .

# restore and publish project in release mode
RUN dotnet restore
RUN dotnet publish -c Release -o ../out

# create lightweight container
FROM mcr.microsoft.com/dotnet/aspnet:6.0

WORKDIR /App/out
COPY --from=build ./App/out .
ADD .env .

## init container
EXPOSE $port
ENTRYPOINT ./entrypoint.sh $devices_db $auth_db $eid $pwd