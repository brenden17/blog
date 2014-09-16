math, fourier transform
푸리에 변환(fourier transform)
scipy, matplotlib, transform

# 파동(Wave)
## 파동이란
[파동](http://ko.wikipedia.org/wiki/%ED%8C%8C%EB%8F%99)은 매질을 통해 운동이나 에너지가 전달되는 현상이다. 쉽게 말해, 흔들림이고 이 흔들림에는 에너지가 있다. 쓰나미를 생각해 보자. 쓰나미는 바다속 어딘가에서 강한 에너지가 생겨 바닷물이라는 매질을 통해 전달되어 생긴다. 빛이 파동이라고 믿던 시절 [마이켈슨-몰리실험](http://ko.wikipedia.org/wiki/%EC%97%90%ED%85%8C%EB%A5%B4_%28%EB%AC%BC%EB%A6%AC%29)으로 빛의 매질이라고 생각했던 에테르(aether)를 찾고자 했다. 물론 에테르를 존재하지 않았고 이 실험은 부정실험으로 유명하다. 빅뱅 이론의 단초가 되었던 은하계가 멀어지고 있는 사실을 어떻게 알았을까? [도플러 효과](http://ko.wikipedia.org/wiki/%EB%8F%84%ED%94%8C%EB%9F%AC_%ED%9A%A8%EA%B3%BC)이다. 빛의 발원지가 이동하면 그 파동의 모양도 변화함에 따라 점점 더 은하계가 멀어지고 있다는 사실을 알았다. 소리, 통신 신호, 나아가면 전자까지도 파동이다. 이렇듯 우리 주변에는 온통 파동이다. 그럼 어떻게 파동을 다룰 수 있을까?

## 푸리에
푸리에(Jean Baptiste Joseph, Baron de Fourier)는 19세기 나폴레옹과 동시대에 살았으며 스승은 라그랑쥐(Joseph Louis Lagrange), 라플라스(Pierre-Simon Laplace)이다. 더욱이 제자는 디리클레(Johann Peter Gustav Lejeune Dirichlet)이다. 말 그대로 새로운 시대의 서막이였다. 푸리에는 제봉사의 아들로 태어났으며 유년기에 부모를 모두 잃었지만 천재성과 달변을 가지고 있었다. 그는 물체를 가열할 때 열이 전달되는 방식을 연구했는데 이때 열이 퍼져 나가는 상태를 파동으로 나타낼 수 있다는 점과 파동의 재미있는 수학적 특성을 알아내었다.

## 푸리에 변환
푸리에 변환 전계는 간략하게 다음과 같다.

 1. 파동은 sin, cos 으로 나타낼 수 있다.
 1. 모든 파동은 sin, cos의 합으로 이루어져 있으며 역으로 파동을 sin, cos으로 나타낼 수 있다(푸리에 급수).
 1. 푸리에 급수에서 계수와 주파수를 구한다.
 1. 이 계수와 주파수가 푸리에 변환이다.
 
더 나아가기 전에 그럼 왜 푸리에 변환이 필요한가. 파동을 sin, cos으로 나타낼 수 있는데 그 특성을 찾거나 처리하기는 쉽지 않다고 한다. 푸리에는 이러한 파동을 여러가지 측면으로 고민하여 특성을 찾아내 푸리에 변환을 만들었다. 이러한 예는 수학사에서 매우 쉽게 찾아 볼 수 있고 이러한 시도가 수학을 좀 더 풍부하고 영역을 넗히게 한 계기이도 하다. 이를테면, 앤드루 와일스는 [페르마의 방정식](http://ko.wikipedia.org/wiki/%ED%8E%98%EB%A5%B4%EB%A7%88%EC%9D%98_%EB%A7%88%EC%A7%80%EB%A7%89_%EC%A0%95%EB%A6%AC)이 타원 방정식으로 변환 가능한 지를 증명하여 증명하였다(사실, 너무 어려운 이야기이다). 어쨌든, 핵심은 해결하고자 하는 문제를 다른 영역으로 변환하여 문제를 푼다는 점이다. 즉, 푸리에 변환에 경우, 시간의 도메인에서 주파수 도메인으로 변환하여 그 특성으로 문제를 바라보게 한다.
몇가지 용어를 정리하자면 다음과 같다.

* 주기(T)  : 파동이 한 번 진동하는데 걸리는 시간
* 주파수(f) : 1초 동안 진동하는 파동의 횟수
* 각속도(w) : 각도 / 시간, 각도 = 각속도 * 시간

sin 곡선과 cos 곡선이 모두 원에서 나온다는 사실을 잊지 말자(오일러 공식의 단초가 된다). 시계 초침이 12시 지점에서 돌기 시작하면 60초 후면 다시 출발한 지점으로 돌아오니 초침의 주파수는 1/60Hz이고 분침은 1/(60*60)Hz이다. 참고로 사람이 들을 수 있는 주파수는 20Hz에서 30,000Hz라고 한다. [Sox](http://sox.sourceforge.net/)를 설치하고 이 대역 주파수를 만들어 들어보자.

    sox --null -r 22050 sine.wav synth 3 sine 20 #20Hz
    sox --null -r 22050 sine.wav synth 3 sine 300 #300Hz
    sox --null -r 22050 sine.wav synth 3 sine 10,000 #10,000Hz
    sox --null -r 22050 sine.wav synth 3 sine 30,000 #10,000Hz
    
쉽게 가청 주파수를 찾을 수 있다. 다음 코드를 사용하여 sin, cos 함수와 FFT를 그릴 수 있다.

    import os
    import glob

    import scipy
    import scipy.io.wavfile
    from scipy import fftpack
    import matplotlib.pyplot as plt

    def plot_wav_fft(wav_filename, desc=None, trans=False):
        plt.clf()
        plt.figure(num=None, figsize=(6, 4))
        sample_rate, X = scipy.io.wavfile.read(wav_filename)
        spectrum = fftpack.fft(X)
        freq = fftpack.fftfreq(len(X), d=1.0 / sample_rate)

        plt.subplot(211)
        num_samples = 300.0
        plt.xlim(0, num_samples / sample_rate)
        plt.xlabel("time [s]")
        plt.title(desc or wav_filename)
        plt.plot(np.arange(num_samples) / sample_rate, X[:num_samples])
        plt.grid(True)

        if trans:
            plt.subplot(212)
            plt.xlim(0, 5000)
            plt.xlabel("frequency [Hz]")
            plt.xticks(np.arange(5) * 4000)
            if desc:
                desc = desc.strip()
                fft_desc = desc[0].lower() + desc[1:]
            else:
                fft_desc = wav_filename
            plt.title("FFT of %s" % fft_desc)
            plt.plot(freq, abs(spectrum), linewidth=2)
            plt.grid(True)
            plt.tight_layout()

        rel_filename = os.path.split(wav_filename)[1]
        plt.savefig("%s_wav_fft.png" % os.path.splitext(rel_filename)[0],
                    bbox_inches='tight')


        plt.show()


    def plot_wav_fft_demo():
        plot_wav_fft("sine_300.wav")
        plot_wav_fft("sine_10000.wav")
        plot_wav_fft("sine_mix.wav")

    plot_wav_fft_demo()

sin 함수를 그려보자.

![alt text](/static/images/sine_300_wav_fft.png "sin300")

주파수와 크기가 다른 sin 함수를 또 그려보자.

![alt text](/static/images/sine_10000_wav_fft.png "sin10000")

이 두 sin 함수를 더하면 어떻께 될까? 단순히 시간마다 y값을 더한 함수가 된다. cos 함수도 같으며 이로서 모든 파동은 sin과 cos 함수를 더하여 나타낼 수 있다.

![alt text](/static/images/sine_mix_wav_fft.png "sin mix")

그러면 반대로 임의 파동을 sin, cos 함수로 분해 할 수 없을까? 이 문제를 해결한 사람이 푸리에이고 임의의 파동을 sin과 cos 함수로 분해한 것이 푸리에 급수가 된다. 이러한 것은 수학에서 자주 볼 수 있다. 푸리에 급수를 나타내면 다음과 같다. 푸리에 급수를 구하는 방법은 그리 어렵지 않다. 도전해 보길 바란다.

$$
f(x)=a_0 + \sum_{n=1}^{\infty }\left ( a_n\cos (nx) + b_n \sin (nx) \right )
$$

이제 푸리에 급수를 구했고 푸리에 급수를 보면 정의되지 않은 값이 있는데 그것이 푸리에 계수이다. 즉, 주파수와 크기이다. 푸리에 계수를 구하면 다음과 같다.

$$
a_0 = \frac{1}{T} \int_{0}^{T} f(t)dt
$$
$$
a_n = \frac{2}{T} \int_{0}^{T} f(t)\cos (nwt)dt
$$
$$
b_n = \frac{2}{T} \int_{0}^{T} f(t)\sin (nwt)dt
$$

여기까지가 끝이다. 시간 도메인으로 나타내던 파동을 주파수 도메인으로 변경하였다. 다시 처음으로 돌아가자. 우리가 처음 보았던 sin 파동을 푸리에 변환해 보자.

![alt text](/static/images/sine_300_wav_fft_.png "sin mix")

다른 주파수의 sin파동도 푸리에 변환해 보자.

![alt text](/static/images/sine_10000_wav_fft_.png "sin10000")

주파수가 다르기 때문에 다른 값이 나온다. 마지막으로 두개가 합해진 파동을 변환하면 두 요소를 볼 수 있다.

![alt text](/static/images/sine_mix_wav_fft_.png "sin mix")

## 활용
파동을 푸리에 변환을 하면 구성하고 있는 주파수로 볼 수 있다. 즉, 파동의 특징을 볼 수 있다는 점이다. 이러한 특징으로 가장 기본적으로 '가', '나', '다'와 같은 기본 음절을 구별할 수 있거나 목소리로 남자와 여자를 구별할 수 있다. 가장 큰 계수를 가지는 주파수 2, 3개를 선택하여 각 음절별로 비교해 보면 차이점 있다. 

## 맺음말
지금까지 파동과 푸리에 변환을 살펴 보았다. 푸리에 변환을 사용하면 소리, 전파와 같은 파동의 특성을 쉽게 파악할 수 있으며, 수학적으로 미분, 적분, 함수의 연속성, 복소수등 다양하게 영향을 미쳤다.