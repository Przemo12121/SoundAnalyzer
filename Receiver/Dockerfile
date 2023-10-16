FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build

# copy project files 
WORKDIR Application/src
ADD . .

# restore and publish project in release mode
RUN dotnet restore
RUN dotnet publish -c Release -o ../out

# create lightweight container
FROM mcr.microsoft.com/dotnet/runtime:7.0

# copy built .dll files and environmental variables
WORKDIR /Application/out
COPY --from=build ./Application/out .
ADD .env .

# init container
ENTRYPOINT ["dotnet", "Receiver.dll"]