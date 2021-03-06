from chatterbox import Chatter, Keyboard, MessageButton, Text

from app.api.logger import logger
from app.api.menu import chef
from app.api.utils import basic_log

chatter = Chatter(memory='sqlite', fallback=True)


@chatter.base(name='홈')
def home_keyboard():
    logger.info('keyboard')

    home_buttons = ['오늘의 식단', '다른 식단 보기', '다른 기능', '의견 보내기']
    return Keyboard(home_buttons)


@chatter.rule(action='다른 기능', src='홈', dest='기타')
@basic_log(cascade=True)
def etc(data):
    text = Text('안녕하세요! 학식알리미 셰프 홍입니다. 무엇을 도와드릴까요?')
    buttons = Keyboard(['자기소개', '추가될 기능', '취소'])
    return text + buttons


@chatter.rule(action='다른 식단 보기', src='홈', dest='다른식단')
@basic_log(cascade=True)
def other(data):
    msg = chef.order('내일')
    text = Text(msg)
    keyboard = Keyboard(['내일의 전체 식단', '내일의 신기숙사', '이번주 식단', '취소'])
    return text + keyboard


@chatter.rule(action='이번주 식단', src='다른식단', dest='홈')
@basic_log(cascade=True)
def other_tomorrow(data):
    text = Text('이번주의 전체 식단은 아래 링크에서 확인할 수 있습니다!')
    msg_button = MessageButton(label='이번주 식단 보기',
                               url='http://apps.hongik.ac.kr/food/food.php')
    keyboard = chatter.home()
    return text + msg_button + keyboard


@chatter.rule(action=['내일의 전체 식단', '내일의 신기숙사'], src='다른식단', dest='홈')
@basic_log(cascade=True)
def other_step2(data):
    content = data.get('content')

    if content == '내일의 전체 식단':
        text = Text(chef.order('내일'))
    if content == '내일의 신기숙사':
        text = Text(chef.order('내일', place='신기숙사'))
    keyboard = chatter.home()
    return text + keyboard


@chatter.rule(action='오늘의 식단', src='홈', dest='오늘식단')
@basic_log(cascade=True)
def today(data):
    msg = chef.order('오늘')
    text = Text(msg)
    keyboard = Keyboard(['전체 식단', '점심', '신기숙사', '취소'])
    return text + keyboard


@chatter.rule(action=['전체 식단', '점심', '신기숙사'], src='오늘식단', dest='홈')
@basic_log('오늘의', cascade=True)
def today_step2(data):
    content = data.get('content')

    if content == '전체 식단':
        text = Text(chef.order('오늘', simplify=False))
    if content == '점심':
        text = Text(chef.order('오늘', time='점심'))
    if content == '신기숙사':
        text = Text(chef.order('오늘', place='신기숙사'))
    keyboard = chatter.home()
    return text + keyboard


@chatter.rule(action='자기소개', src='기타', dest='홈')
@basic_log(cascade=True)
def intro(data):
    text = Text(
        '학식알리미 셰프 홍은 여기서 개발되고 있어요! '
        '기능 제안, 버그 제보는 언제나 환영합니다. (최고)\n'
        '개발자 분들이 (별) 눌러주시길 기대할게요!')
    msg_button = MessageButton(label='이동하기',
                               url='https://github.com/jungwinter/chef-hong')
    keyboard = chatter.home()
    return text + msg_button + keyboard


@chatter.rule(action='추가될 기능', src='기타', dest='홈')
@basic_log(cascade=True)
def roadmap(data):
    text = Text(
        '앞으로 다양한 기능이 추가 될 예정입니다!\n'
        '* 학식 사진으로 보기\n'
        '* 커뮤니티\n'
        '* 이 달의 최고 학식러\n'
        '\n'
        '기능 제안은 언제나 환영합니다! 개발자에게 연락해주세요!')
    msg_button = MessageButton(label='개발자 트위터',
                               url='https://twitter.com/res_tin')
    keyboard = chatter.home()
    return text + msg_button + keyboard


@chatter.rule(action='취소', src='*', dest='홈')
@basic_log(cascade=True)
def cancel(data):
    text = Text('취소하셨습니다. 다른 기능도 이용해보세요!')
    return text + chatter.home()


@chatter.rule(action='의견 보내기', src='홈', dest='의견')
@basic_log(cascade=True)
def opinion(data):
    text = Text(
        '아무말이나 보내주셔도 괜찮습니다! 개발자가 직접 확인하겠습니다 (최고)\n'
        '* 개발자는 학식 업체나 학교 직원이 아닙니다. 참고해주세요!')
    keyboard = Keyboard(type='text')
    return text + keyboard


@chatter.rule(action='*', src='의견', dest='홈')
def listen(data):
    answer = data.get('content')
    logger.info(answer, extra=dict(text=answer))
    text = Text(
        '의견을 보내주셔서 감사합니다! 다른 건의사항이나 의견이 있으시다면 '
        '또 보내주셔도 좋습니다 (굿)')
    return text + chatter.home()


def error():
    text = Text('알 수 없는 오류가 발생했습니다!\n이번주 식단 기능만 활성화됩니다.')
    msg_button = MessageButton(label='이번주 식단 보기',
                               url='http://apps.hongik.ac.kr/food/food.php')
    return text + msg_button + chatter.home()
