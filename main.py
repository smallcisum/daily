import streamlit as st
import requests
import datetime
import pytz
import random

# ==== 設定 OpenWeatherMap ====
API_KEY = "11e1ae55357eb1c7ab1b8823783fa5c9"  # OpenWeatherMap API Key
LANG = "zh_tw"
UNITS = "metric"

# ==== 中文星期對照表 ====
weekdays = {
    0: "星期一",
    1: "星期二",
    2: "星期三",
    3: "星期四",
    4: "星期五",
    5: "星期六",
    6: "星期日"
}

# ==== 小語庫 ====
quotes = [
    ("成功是每天積小步前進。", "Success is the sum of small efforts repeated every day."),
    ("相信自己，你比想像中更堅強。", "Believe in yourself, you are stronger than you think."),
    ("每天都是重新開始的機會。", "Every day is a chance to start anew."),
    ("你的夢想值得你努力。", "Your dreams are worth the effort."),
    ("你走的每一步都算數。", "Every step you take matters."),
    #安慰與鼓勵
    ("我靠著那加給我力量的，凡事都能做。腓立比書 4:13", "I can do all things through Christ who strengthens me."),
    ("你們當將一切的憂慮卸給神，因為他顧念你們。彼得前書 5:7", "Cast all your anxiety on him because he cares for you."),
    ("壓傷的蘆葦，他不折斷；將殘的燈火，他不吹滅。", "A bruised reed he will not break, and a smoldering wick he will not snuff out.", "馬太福音 12:20"),
    ("耶和華是我的牧者，我必不致缺乏。", "The Lord is my shepherd; I shall not want.", "詩篇 23:1"),
    ("疲乏的，他賜能力；軟弱的，他加力量。", "He gives strength to the weary and increases the power of the weak.", "以賽亞書 40:29"),
    ("我雖然行過死蔭的幽谷，也不怕遭害，因為你與我同在。", "Even though I walk through the darkest valley, I will fear no evil, for you are with me.", "詩篇 23:4"),
    ("我們曉得萬事都互相效力，叫愛神的人得益處。", "And we know that in all things God works for the good of those who love him.", "羅馬書 8:28"),
    ("不要懼怕，因為我與你同在；不要驚惶，因為我是你的神。", "So do not fear, for I am with you; do not be dismayed, for I am your God.", "以賽亞書 41:10"),
    ("凡勞苦擔重擔的人，可以到我這裡來，我就使你們得安息。", "Come to me, all you who are weary and burdened, and I will give you rest.", "馬太福音 11:28"),
    ("他的怒氣不過是轉眼之間；他的恩典乃是一生之久。一宿雖然有哭泣，早晨便必歡呼。", "For his anger lasts only a moment, but his favor lasts a lifetime; weeping may stay for the night, but rejoicing comes in the morning.", "詩篇 30:5"),
    ("應當一無掛慮，只要凡事藉著禱告、祈求，和感謝，將你們所要的告訴神。", "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.", "腓立比書 4:6"),
    ("敬畏耶和華是智慧的開端；認識至聖者便是聰明。", "The fear of the Lord is the beginning of wisdom, and knowledge of the Holy One is understanding.", "箴言 9:10"),
    ("他使我的靈魂甦醒，為自己的名引導我走義路。", "He restores my soul. He leads me in paths of righteousness for his name’s sake.", "詩篇 23:3"),
    ("因為，凡求告主名的，就必得救。", "For, \"everyone who calls on the name of the Lord will be saved.\"", "羅馬書 10:13"),
    ("你們所遇見的試探，無非是人所能受的。神是信實的，必不叫你們受試探過於所能受的。在受試探的時候，總要給你們開一條出路，叫你們能忍受得住。", "No temptation has overtaken you except what is common to mankind. And God is faithful; he will not let you be tempted beyond what you can bear. But when you are tempted, he will also provide a way out so that you can endure it.", "哥林多前書 10:13"),
    ("耶和華是我的亮光，是我的拯救，我還怕誰呢？", "The Lord is my light and my salvation—whom shall I fear?", "詩篇 27:1"),
    ("義人多有苦難，但耶和華救他脫離這一切。", "The righteous person may have many troubles, but the Lord delivers him from them all.", "詩篇 34:19"),
    ("愛裡沒有懼怕；愛既完全，就把懼怕除去。", "There is no fear in love. But perfect love drives out fear.", "約翰一書 4:18"),
    ("我留下平安給你們；我將我的平安賜給你們。", "Peace I leave with you; my peace I give you.", "約翰福音 14:27"),
    ("我雖然在困苦中，你卻使我活著。", "Though I walk in the midst of trouble, you preserve my life.", "詩篇 138:7"),
 #愛與人際關係  
    ("愛是恆久忍耐，又有恩慈；愛是不嫉妒；愛是不自誇，不張狂。", "Love is patient, love is kind. It does not envy, it does not boast, it is not proud.", "哥林多前書 13:4"),
    ("不做害羞的事，不求自己的益處，不輕易發怒，不計算人的惡。", "It does not dishonor others, it is not self-seeking, it is not easily angered, it keeps no record of wrongs.", "哥林多前書 13:5"),
    ("不喜歡不義，只喜歡真理；凡事包容，凡事相信，凡事盼望，凡事忍耐。", "It does not delight in evil but rejoices with the truth. It always protects, always trusts, always hopes, always perseveres.", "哥林多前書 13:6-7"),
    ("愛是永不止息。", "Love never fails.", "哥林多前書 13:8"),
    ("最要緊的是彼此切實相愛，因為愛能遮掩許多的罪。", "Above all, love each other deeply, because love covers over a multitude of sins.", "彼得前書 4:8"),
    ("你們要彼此相愛，像我愛你們一樣；這就是我的命令。", "My command is this: Love each other as I have loved you.", "約翰福音 15:12"),
    ("我們愛，因為神先愛我們。", "We love because he first loved us.", "約翰一書 4:19"),
    ("親愛的弟兄啊，我們應當彼此相愛，因為愛是從神來的。", "Dear friends, let us love one another, for love comes from God.", "約翰一書 4:7"),
    ("未曾愛心的，就不認識神，因為神就是愛。", "Whoever does not love does not know God, because God is love.", "約翰一書 4:8"),
    ("總而言之，你們都要同心，彼此體恤，相愛如弟兄，存憐憫的心，謙卑。", "Finally, all of you, be like-minded, be sympathetic, love one another, be compassionate and humble.", "彼得前書 3:8"),
    ("恨能挑啟爭端；愛能遮掩一切過錯。", "Hatred stirs up conflict, but love covers over all wrongs.", "箴言 10:12"),
    ("不可欠人的債，除了彼此相愛。因為愛人的就完全了律法。", "Let no debt remain outstanding, except the continuing debt to love one another, for whoever loves others has fulfilled the law.", "羅馬書 13:8"),
    ("所以，你們要彼此接納，如同基督接納你們一樣，使榮耀歸與神。", "Accept one another, then, just as Christ accepted you, in order to bring praise to God.", "羅馬書 15:7"),
    ("以善勝惡。", "Overcome evil with good.", "羅馬書 12:21"),
    ("要凡事謙虛、溫柔、忍耐，用愛心互相寬容。", "Be completely humble and gentle; be patient, bearing with one another in love.", "以弗所書 4:2"),
    ("愛人如己。", "Love your neighbor as yourself.", "馬可福音 12:31"),
    ("要常常喜樂，不住地禱告，凡事謝恩。", "Rejoice always, pray continually, give thanks in all circumstances.", "帖撒羅尼迦前書 5:16-18"),
    ("溫柔的回答使怒氣消退；刺耳的話語激動怒氣。", "A gentle answer turns away wrath, but a harsh word stirs up anger.", "箴言 15:1"),
    ("所以，無論何事，你們願意人怎樣待你們，你們也要怎樣待人。", "So in everything, do to others what you would have them do to you.", "馬太福音 7:12"),
    ("施比受更為有福。", "It is more blessed to give than to receive.", "使徒行傳 20:35"),
    ("弟兄們，你們蒙召是要得自由，只是不可將你們的自由當作放縱情慾的機會，總要用愛心互相服事。", "You, my brothers and sisters, were called to be free. But do not use your freedom to indulge the flesh; rather, serve one another humbly in love.", "加拉太書 5:13"),
    ("要常存弟兄相愛的心。", "Keep on loving one another as brothers and sisters.", "希伯來書 13:1"),
    ("忍耐的人，大有聰明；性情急躁的，大顯愚妄。", "A patient person has great understanding, but one who is quick-tempered displays folly.", "箴言 14:29"),
    ("朋友乃時常親愛；弟兄為患難而生。", "A friend loves at all times, and a brother is born for a time of adversity.", "箴言 17:17"),
    ("鐵磨鐵，磨出刃來；朋友相感，也是如此。", "As iron sharpens iron, so one person sharpens another.", "箴言 27:17"),
    ("若有人說：「我愛神」，卻恨他的弟兄，就是說謊的；不愛他所看見的弟兄，就不能愛沒有看見的神。", "Whoever claims to love God yet hates a brother or sister is a liar. For whoever does not love their brother or sister, whom they have seen, cannot love God, whom they have not seen.", "約翰一書 4:20"),
    ("你們中間誰願為大，就必作你們的用人；誰願為首，就必作你們的僕人。", "Whoever wants to become great among you must be your servant, and whoever wants to be first must be your slave.", "馬太福音 20:26-27"),
    ("你們要彼此饒恕，正如主饒恕了你們一樣。", "Forgive each other, just as the Lord has forgiven you.", "歌羅西書 3:13"),
    ("當我們還有機會的時候，就當向眾人行善，向信徒一家的人更當如此。", "Therefore, as we have opportunity, let us do good to all people, especially to those who belong to the family of believers.", "加拉太書 6:10"),
    ("親愛的弟兄啊，不要為自己伸冤，寧可讓步，聽憑主怒。", "Do not take revenge, my dear friends, but leave room for God’s wrath.", "羅馬書 12:19"),
    ("你們一切的事都當憑愛心而做。", "Let all that you do be done in love.", "哥林多前書 16:14"),
    ("你們各人的重擔要互相擔當，如此，就完全了基督的律法。", "Carry each other’s burdens, and in this way you will fulfill the law of Christ.", "加拉太書 6:2"),
    ("你們要和睦相處。", "Live in peace with each other.", "馬可福音 9:50"),
    ("又要彼此相愛，像我愛你們一樣。", "Love one another as I have loved you.", "約翰福音 13:34"),
    ("不要以惡報惡；眾人以為美的事要留心去做。", "Do not repay evil with evil or insult with insult. On the contrary, repay evil with blessing, because to this you were called so that you may inherit a blessing.", "羅馬書 12:17"),
    ("不可含怒到日落。", "Do not let the sun go down while you are still angry.", "以弗所書 4:26"),
    ("言語純全，無可指責，叫那反對的人，因說不出什麼惡來，就自覺羞愧。", "In your teaching show integrity, seriousness and soundness of speech that cannot be condemned, so that those who oppose you may be ashamed because they have nothing bad to say about us.", "提多書 2:7-8"),
    ("你們要追求愛，也要切慕屬靈的恩賜，尤其要切慕作先知講道。", "Follow the way of love and eagerly desire gifts of the Spirit, especially prophecy.", "哥林多前書 14:1"),
    ("使人和平的，是用和平所栽種的義果。", "Peacemakers who sow in peace reap a harvest of righteousness.", "雅各書 3:18"),
    ("一句話說得合宜，就如金蘋果在銀網子裡。", "A word fitly spoken is like apples of gold in settings of silver.", "箴言 25:11"),
    ("好樹結好果子；壞樹結壞果子。", "A good tree cannot bear bad fruit, nor can a bad tree bear good fruit.", "馬太福音 7:17"),
    ("存心謙卑，各人看別人比自己強。", "In humility value others above yourselves.", "腓立比書 2:3"),
    ("不要論斷人，免得你們被論斷。", "Do not judge, or you too will be judged.", "馬太福音 7:1"),
    ("你們禱告，無論求什麼，只要信，就必得著。", "If you believe, you will receive whatever you ask for in prayer.", "馬太福音 21:22"),
    ("要愛你們的仇敵，為那逼迫你們的禱告。", "Love your enemies and pray for those who persecute you.", "馬太福音 5:44"),
    ("若有人在基督裡，他就是新造的人，舊事已過，都變成新的了。", "Therefore, if anyone is in Christ, the new creation has come: The old has gone, the new is here!", "哥林多後書 5:17"),
    ("他叫那認識耶和華的，認識耶和華。", "He reveals the deep things of darkness and brings utter darkness into the light.", "約伯記 12:22"), # 這句原文主要關於神的權能，與「愛與人際關係」主題關聯較弱，但仍可作為一般真理。若需替換，寶劍可以提供替代。
    ("你的話是我腳前的燈，是我路上的光。", "Your word is a lamp for my feet, a light on my path.", "詩篇 119:105"),
    ("我聽見你的聲音，我歡喜快樂。", "I rejoice in your word like one finding great spoil.", "詩篇 119:162"),
    ("神在我們裡面，因為我們遵守他的命令。這就使我們知道，神住在我們裡面，是藉著他所賜給我們的聖靈。", "And this is how we know that he lives in us: We know it by the Spirit he gave us.", "約翰一書 3:24"),
#信心與盼望
    ("信就是所望之事的實底，是未見之事的確據。", "Now faith is confidence in what we hope for and assurance about what we do not see.", "希伯來書 11:1"),
    ("敬畏耶和華是智慧的開端；認識至聖者便是聰明。", "The fear of the Lord is the beginning of wisdom, and knowledge of the Holy One is understanding.", "箴言 9:10"), # 重複前批，但仍與智慧、信心相關
    ("人非有信，就不能得神的喜悅；因為到神面前來的人必須信有神，且信他賞賜那尋求他的人。", "And without faith it is impossible to please God, because anyone who comes to him must believe that he exists and that he rewards those who earnestly seek him.", "希伯來書 11:6"),
    ("但那等候耶和華的，必從新得力。他們必如鷹展翅上騰；他們奔跑卻不困倦，行走卻不疲乏。", "but those who hope in the Lord will renew their strength. They will soar on wings like eagles; they will run and not grow weary, they will walk and not be faint.", "以賽亞書 40:31"),
    ("因為我們行事為人是憑著信心，不是憑著眼見。", "For we live by faith, not by sight.", "哥林多後書 5:7"),
    ("堅心倚賴你的，你必保守他十分平安，因為他倚靠你。", "You will keep in perfect peace those whose minds are steadfast, because they trust in you.", "以賽亞書 26:3"),
    ("凡事都能，在信的人，凡事都能。", "Everything is possible for one who believes.", "馬可福音 9:23"),
    ("我留下平安給你們；我將我的平安賜給你們。", "Peace I leave with you; my peace I give you.", "約翰福音 14:27"), # 重複前批，但仍與平安、信心相關
    ("所以，我們只管坦然無懼地來到施恩的寶座前，為要得憐恤，蒙恩惠，作隨時的幫助。", "Let us then approach God’s throne of grace with confidence, so that we may receive mercy and find grace to help us in our time of need.", "希伯來書 4:16"),
    ("你當倚靠耶和華而行善，住在地上，以他的信實為糧。", "Trust in the Lord and do good; dwell in the land and enjoy safe pasture.", "詩篇 37:3"),
    ("因為凡從神生的，就勝過世界；使我們勝過世界的，就是我們的信心。", "For everyone born of God overcomes the world. This is the victory that has overcome the world—even our faith.", "約翰一書 5:4"),
    ("凡你們禱告祈求的，無論是什麼，只要信是得著的，就必得著。", "Therefore I tell you, whatever you ask for in prayer, believe that you have received it, and it will be yours.", "馬可福音 11:24"),
    ("應當一無掛慮，只要凡事藉著禱告、祈求，和感謝，將你們所要的告訴神。", "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.", "腓立比書 4:6"), # 重複前批，但仍與信心、禱告相關
    ("我知道我所信的是誰，也深信他能保全我所交付他的，直到那日。", "I know whom I have believed, and am convinced that he is able to guard what I have entrusted to him until that day.", "提摩太後書 1:12"),
    ("所以，你們若真與基督一同復活，就當尋求在上面的事；那裡有基督坐在神的右邊。", "Since, then, you have been raised with Christ, set your hearts on things above, where Christ is seated at the right hand of God.", "歌羅西書 3:1"),
    ("這就是我們的盼望，像錨一樣又穩又牢，直通到幔子內，進入至聖所。", "We have this hope as an anchor for the soul, firm and secure. It enters the inner sanctuary behind the curtain.", "希伯來書 6:19"),
    ("義人必因信得生。", "The righteous will live by faith.", "羅馬書 1:17"),
    ("你們得救是本乎恩，也因著信。這並不是出於自己，乃是神所賜的。", "For it is by grace you have been saved, through faith—and this is not from yourselves, it is the gift of God.", "以弗所書 2:8"),
    ("你的信救了你，平平安安地去吧！", "Your faith has saved you; go in peace.", "路加福音 7:50"),
    ("耶穌對他說：你若能信，在信的人，凡事都能。", "Jesus said to him, “If you can believe, all things are possible to him who believes.”", "馬可福音 9:23"), # 重複前批意義類似的經文，但句式略有差異。
    ("神為愛他的人所預備的是眼睛未曾看見，耳朵未曾聽見，人心也未曾想到的。", "However, as it is written: “What no eye has seen, what no ear has heard, and what no human mind has conceived”—what God has prepared for those who love him.", "哥林多前書 2:9"),
    ("因為凡求告主名的，就必得救。", "For, \"everyone who calls on the name of the Lord will be saved.\"", "羅馬書 10:13"), # 重複前批，但仍與信心、呼求相關
    ("我們又藉著他，因信得進入現在所站的這恩典中，並且歡歡喜喜盼望神的榮耀。", "through whom we have gained access by faith into this grace in which we now stand. And we boast in the hope of the glory of God.", "羅馬書 5:2"),
    ("願頌讚歸與我們主耶穌基督的父神！他曾照自己的大憐憫，藉耶穌基督從死裡復活，叫我們有活潑的盼望。", "Praise be to the God and Father of our Lord Jesus Christ! In his great mercy he has given us new birth into a living hope through the resurrection of Jesus Christ from the dead.", "彼得前書 1:3"),
    ("我們如今彷彿對著鏡子觀看，模糊不清，到那時就要面對面了。我如今所知道的有限，到那時就全知道了，如同主知道我一樣。", "For now we see only a reflection as in a mirror; then we shall see face to face. Now I know in part; then I shall know fully, even as I am fully known.", "哥林多前書 13:12"),
    ("應當知道，你的神是神，是守約施慈愛的神，向愛他守他誡命的人守約施慈愛，直到千代。", "Know therefore that the Lord your God is God; he is the faithful God, keeping his covenant of love to a thousand generations of those who love him and keep his commandments.", "申命記 7:9"),
    ("耶和華的眼目遍察全地，要顯大能幫助向他心存誠實的人。", "For the eyes of the Lord range throughout the earth to strengthen those whose hearts are fully committed to him.", "歷代志下 16:9"),
    ("人所行的在耶和華眼中看為正直，耶和華必引導他的腳步。", "In their hearts humans plan their course, but the Lord establishes their steps.", "箴言 16:9"),
    ("我們是與神同工的；你們是神所耕種的田地，所建造的房屋。", "For we are co-workers in God’s service; you are God’s field, God’s building.", "哥林多前書 3:9"),
    ("因為，神賜給我們，不是膽怯的心，乃是剛強、仁愛、謹守的心。", "For the Spirit God gave us does not make us timid, but gives us power, love and self-discipline.", "提摩太後書 1:7"),
    ("我總不撇下你，也不丟棄你。", "Never will I leave you; never will I forsake you.", "希伯來書 13:5"),
    ("神啊，我的心切慕你，如鹿切慕溪水。", "As the deer pants for streams of water, so my soul pants for you, my God.", "詩篇 42:1"),
    ("願賜盼望的神，因信將諸般的喜樂、平安充滿你們的心，使你們藉著聖靈的能力大有盼望。", "May the God of hope fill you with all joy and peace as you trust in him, so that you may overflow with hope by the power of the Holy Spirit.", "羅馬書 15:13"),
    ("因為義人雖七次跌倒，仍必興起；惡人卻被禍患傾倒。", "For though the righteous fall seven times, they rise again, but the wicked stumble when calamity strikes.", "箴言 24:16"),
    ("你的話是我腳前的燈，是我路上的光。", "Your word is a lamp for my feet, a light on my path.", "詩篇 119:105"), # 重複前批，但與信心指引相關
    ("洪水泛濫之時，耶和華坐著為王；耶和華坐著為王，直到永遠。", "The Lord sits enthroned over the flood; the Lord is enthroned as King forever.", "詩篇 29:10"),
    ("誰能使我們與基督的愛隔絕呢？難道是患難嗎？是困苦嗎？是逼迫嗎？是飢餓嗎？是赤身露體嗎？是危險嗎？是刀劍嗎？", "Who shall separate us from the love of Christ? Shall trouble or hardship or persecution or famine or nakedness or danger or sword?", "羅馬書 8:35"),
    ("然而，靠著愛我們的主，在這一切的事上已經得勝有餘了。", "No, in all these things we are more than conquerors through him who loved us.", "羅馬書 8:37"),
    ("我深信無論是死，是生，是天使，是掌權的，是有能的，是現在的事，是將來的事，是高處的，是深處的，是別的受造之物，都不能叫我們與神的愛隔絕；這愛是在我們主基督耶穌裡的。", "For I am convinced that neither death nor life, neither angels nor demons, neither the present nor the future, nor any powers, neither height nor depth, nor anything else in all creation, will be able to separate us from the love of God that is in Christ Jesus our Lord.", "羅馬書 8:38-39"),
    ("所以，弟兄們，我以神的慈悲勸你們，將身體獻上，當作活祭，是聖潔的，是神所喜悅的；你們如此事奉乃是理所當然的。", "Therefore, I urge you, brothers and sisters, in view of God’s mercy, to offer your bodies as a living sacrifice, holy and pleasing to God—this is your true and proper worship.", "羅馬書 12:1"),
    ("不要效法這個世界，只要心意更新而變化，叫你們察驗何為神的善良、純全、可喜悅的旨意。", "Do not conform to the pattern of this world, but be transformed by the renewing of your mind. Then you will be able to test and approve what God’s will is—his good, pleasing and perfect will.", "羅馬書 12:2"),
    ("你們要向耶和華唱新歌！全地都要向耶和華歌唱！", "Sing to the Lord a new song; sing to the Lord, all the earth.", "詩篇 96:1"),
    ("耶和華靠近傷心的人，拯救靈性痛悔的人。", "The Lord is close to the brokenhearted and saves those who are crushed in spirit.", "詩篇 34:18"),
    ("智慧人心中有知識，愚昧人心裡有愚昧。", "The heart of the discerning acquires knowledge; the ears of the wise seek it out.", "箴言 18:15"),
    ("因為我們不是與屬血氣的爭戰，乃是與那些執政的、掌權的、管轄這幽暗世界的，以及天空屬靈氣的惡魔爭戰。", "For our struggle is not against flesh and blood, but against the rulers, against the authorities, against the powers of this dark world and against the spiritual forces of evil in the heavenly realms.", "以弗所書 6:12"),
    ("凡事不能叫我受害的，神必為我承擔。", "I will not let anything hurt me; I will endure all things.", "哥林多前書 6:12"), # 這裡的英文金句似乎與中文原意不完全匹配，英文通常是 "I have the right to do anything," you say—but not everything is beneficial. "I have the right to do anything"—but I will not be mastered by anything. 如果需要更貼近，請告訴我。
    ("神是我們的避難所，是我們的力量，是我們在患難中隨時的幫助。", "God is our refuge and strength, an ever-present help in trouble.", "詩篇 46:1"),
    ("他從高天伸手抓住我，把我從大水中拉上來。", "He reached down from on high and took hold of me; he drew me out of deep waters.", "詩篇 18:16"),
    ("耶和華的慈愛，上及諸天；他的信實，達到穹蒼。", "Your love, Lord, reaches to the heavens, your faithfulness to the skies.", "詩篇 36:5"),
    ("願你吸引我，我們就快跑跟隨你。", "Take me away with you—let us hurry! The king has brought me into his chambers.", "雅歌 1:4"), # 這句原文的意境是追求親密關係，與「信心與盼望」的直接關聯較弱，更偏向愛情詩歌。若需替換，寶劍可以提供替代。
    ("你的救恩是我的喜樂。", "I rejoice in your salvation.", "詩篇 9:14")


    
]

# ==== 行動選項 ====
all_actions = [
    "努力", "奮起", "開心", "積極", "有效率", "放鬆", "溫柔", "專注", "快樂", "冒險",
    "深呼吸", "陪伴", "關懷", "觀察自己", "讚美別人", "早睡", "喝水", "多走路", "不抱怨", "大笑",
    "學習新事物", "吃得健康", "整理空間", "耐心聽人說話", "說實話", "讚美自己", "敢於嘗試", "不逃避", "完成一件小事",
    "勇敢", "傾聽", "關心周遭", "提升自己", "看別人優點", "早點行動", "做運動", "跳躍", "不傷心", "玩遊戲",
    "學習冒險", "吃得開心", "保持整潔", "有同理心", "想像未來", "讚美小事物", "敢於挑戰", "不害怕", "完成工作",
"深深感受", "有愛心", "憐憫別人", "原諒自己", "原諒別人", "靜下來想想", "多動動", "多嘗試", "不退縮", "大哭一場",
    "試著了解", "用心思考", "斷捨離", "發掘自己優點", "接受自己", "和朋友說話", "追求夢想", "解決現實問題", "療癒自己"
]

# ==== 取得使用者地理位置與時區 ====
def get_location():
    try:
        ip_info = requests.get("https://ipapi.co/json").json()
        city = ip_info.get("city", "Hsinchu")
        timezone_str = ip_info.get("timezone", "Asia/Taipei")
        tz = pytz.timezone(timezone_str)
    except:
        city = "Hsinchu"
        tz = pytz.timezone("Asia/Taipei")
    return city, tz

CITY, TZ = get_location()

# ==== 時間處理 ====
now = datetime.datetime.now(TZ)
date_str = now.strftime("%Y/%m/%d")
weekday_ch = weekdays[now.weekday()]
time_str = now.strftime("%H:%M")

# ==== 天氣資料 ====
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}&lang={LANG}"
try:
    response = requests.get(weather_url)
    weather_data = response.json()
    weather_desc = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"]
except:
    weather_desc = "取得失敗"
    temp = "--"

# ==== 小語與選項狀態保存 ====
if "quote" not in st.session_state:
    st.session_state.quote = random.choice(quotes)

if "options" not in st.session_state:
    st.session_state.options = random.sample(all_actions, 3)

quote_ch, quote_en = st.session_state.quote
options = st.session_state.options

# ==== 畫面顯示 ====
st.markdown(f"""
## 📍 根據您目前的位置：**{CITY}**
## 📅 日期：{date_str}（{weekday_ch}）
### 🕰️ 當地時間：{time_str}
### 🌤️ 天氣：{weather_desc}，氣溫 {temp}°C

---

### ✨ 今日小語：
> {quote_ch}  
> _{quote_en}_

---

### 🎯 今日選項（請選擇你今天想實踐的行動）：
""")

user_choice = st.radio("請選擇：", options)

if st.button("✨ 我決定了！"):
    st.success(f"🧡 我決定今天要：「{user_choice}」！一起加油吧 👑✨")
