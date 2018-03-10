#!/usr/bin/fish

for app in {audio,plate,scale,yolo}
    docker build -t recolic/tfapp-$app:latest -f $app.dockerfile .
end
for app in {audio,plate,scale,yolo}
    docker push recolic/tfapp-$app:latest
end

git add -A
git commit -m 'update'
git push
