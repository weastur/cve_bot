.PHONY: release build clean push py_build py_push docker_build docker_push
VERSION=`python -c "import cve_bot; print(cve_bot.__version__)"`

release: push

push: py_push docker_push

build: py_build docker_build

py_build: clean
	python -m build

docker_build: clean
	docker build . --build-arg=VERSION=${VERSION} -t weastur/cve_bot:latest -t weastur/cve_bot:${VERSION}

py_push: py_build
	twine upload dist/cve_bot-${VERSION}*

docker_push: docker_build
	docker push weastur/cve_bot:latest
	docker push weastur/cve_bot:${VERSION}

clean:
	rm -rf build/ cve_bot.egg-info/ dist
