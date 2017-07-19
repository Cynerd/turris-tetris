#!/bin/sh

git add .
git ci --amend -C HEAD
git rev-parse HEAD | clip
git push -f
