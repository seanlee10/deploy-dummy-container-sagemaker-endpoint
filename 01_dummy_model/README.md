# 임의의 추론 모델을 커스텀 컨테이너 이미지로 만들어 Sagemaker에 배포하기

**커스텀 컨테이너 이미지 빌드와 SageMaker Endpoint 배포** 기본 과정을 익힐 수 있도록, 이 프로젝트에서는 간단한 더미 컨테이너 이미지를 만들고 이를 Sagemaker로 배포하는 과정을 안내합니다. 
이번 실습에서 다룰 내용은 다음과 같습니다. 

1. 컨테이너 이미지는 실제 학습 모델을 구현하는 대신, 추론 요청에 대해 임의의 정적 값을 반환하도록 구현합니다. 
2. SageMaker에서 권장하는 방식인 nginx → gunicorn → wsgi → flask 구조가 아닌, Flask 단독으로 추론 모델을 서빙합니다. 

이 구성은 실제 서비스에 적합하지는 않지만, SageMaker Endpoint가 컨테이너 이미지를 다루는 메커니즘을 이해하는 데에 도움을 줍니다.


## 실행 안내

### 1. ECR에 커스텀 컨테이너 이미지 등록하기
predictor.py를 ECR에 배포하기 위한 방법은 아래와 같습니다. 
```shell
$ chmod +x ./build_and_push.sh 
$ ./build_and_push.sh <등록할 임의의 컨테이너 이미지명>  
```

### 2. 등록된 컨테이너 이미지를 Sagemaker Endpoint로 배포하기 
커스텀 컨테이너 이미지를 Sagemaker Endpoint로 배포하려면 아래와 같은 3단계를 거쳐야 합니다. 

- Sagemaker Model 등록하기
- Sagemaker Endpoint Config 등록하기
- Sagemaker Endpoint 등록하기

해당 과정은 다음 파일에 자세히 설명되어 있으므로 참고하시기 바랍니다. 
- deploy_container_image.ipynb
