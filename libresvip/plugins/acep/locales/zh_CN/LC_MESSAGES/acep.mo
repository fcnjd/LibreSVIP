Þ    +      t              Ì  ³   Í       a     s  û     o          ¨  -   °     Þ     ù          (     G     O     f     ~       "   ¢     Å  g   Õ  d   =  c   ¢  &        -     ;  1   H  7   z  ©  ²     \
  #   d
     
  Z  ¨
  =    =  A  ?    Q  ¿          )    E  c   Ñ  e   5  	       ¥     0     ±  P   É  O       j      z         #         Á   !   à      !     !     4!     ;!     N!     a!     w!     ~!     !  V   ¤!  H   û!  H   D"     "  	   ¦"  	   °"  '   º"  0   â"  !  #     5$     B$     \$    x$  -  %  Z  Ã(  Z  ,    y/     |0     0  8  ¨0  ~   á1  E   `2     ¦2   ACE Studio has both strength and tension parameters, both of which can affect the strength of the singing. This option is used to set the mapping target of the strength parameter. ACE Studio project File ACE Studio supports three languages of lyrics. This option is used to set the language of lyrics. ACE Studio will add pronunciation to all notes. This is a redundant data for most Chinese characters, so by default only modified pronunciation will be kept. When this option is turned on, all pronunciation information will be kept unconditionally, but it may produce a larger file size. When the source file contains non-Chinese singing data, please turn on this option. Both strength and tension Breath parameter normalization Chinese Conversion Plugin for ACE Studio project file Default breath length (ms) Default consonant length (secs) Default singer Energy parameter normalization English Import energy envelope Import tension envelope Interval of curve sampling Japanese Keep all pronunciation information Lyrics language Map both strength and tension parameters to strength and tension parameters, each with a weight of 50%. Map only strength parameters to strength parameters. Tension parameters will remain unparameterized. Map only tension parameters to tension parameters. Strength parameters will remain unparameterized. Map strength and tension parameters to Only strength Only tension Please input the complete and correct singer name Set default consonant length for notes if not specified Since the strength parameter of ACE Studio has a significant impact on the volume, this option is provided to control the mapping coefficient of the strength envelope. The strength envelope will be multiplied by the value of this option as a whole and then mapped to the volume channel of the intermediate model, and the remaining part will be mapped to the strength channel. This option accepts values in the range of 0~1.0. Spanish Strength-volume mapping coefficient Tension parameter normalization The unit is tick (the length of a quarter note is 480 ticks). By default, the parameter points in the acep file are stored in a very dense manner. Increasing the sampling interval appropriately will not cause much loss of accuracy, but it can get a smaller file size. Setting to 0 or a negative value means keeping the original sampling interval. This option is an advanced option. After enabling this option, the breath parameters will be merged with the breath envelope after being transformed by the normalization. It is recommended to enable this option after fixing all parameters with a fixed brush. This option needs to set 5 values, separated by "," from each other:
(1) Normalization method: none means to turn off this option, zscore means to perform Z-Score normalization on the parameter points, and minmax means to Min-Max normalize the parameter points to the [-1.0, 1.0] interval.
(2) Lower threshold: a real number in the range of 0~10.0, the parameter points lower than this value will not participate in the normalization.
(3) Upper threshold: a real number in the range of 0~10.0, the parameter points higher than this value will not participate in the normalization.
(4) Scaling factor: a real number in the range of -1.0~1.0, the normalized parameter value will be multiplied by this value.
(5) Bias: a real number in the range of -1.0~1.0, the normalized and scaled parameter value will be added to this value. This option is an advanced option. After enabling this option, the energy parameters will be merged with the energy envelope after being transformed by the normalization. It is recommended to enable this option after fixing all parameters with a fixed brush. This option needs to set 5 values, separated by "," from each other:
(1) Normalization method: none means to turn off this option, zscore means to perform Z-Score normalization on the parameter points, and minmax means to Min-Max normalize the parameter points to the [-1.0, 1.0] interval.
(2) Lower threshold: a real number in the range of 0~10.0, the parameter points lower than this value will not participate in the normalization.
(3) Upper threshold: a real number in the range of 0~10.0, the parameter points higher than this value will not participate in the normalization.
(4) Scaling factor: a real number in the range of -1.0~1.0, the normalized parameter value will be multiplied by this value.
(5) Bias: a real number in the range of -1.0~1.0, the normalized and scaled parameter value will be added to this value. This option is an advanced option. After enabling this option, the tension parameters will be merged with the tension envelope after being transformed by the normalization. It is recommended to enable this option after fixing all parameters with a fixed brush. This option needs to set 5 values, separated by "," from each other:
(1) Normalization method: none means to turn off this option, zscore means to perform Z-Score normalization on the parameter points, and minmax means to Min-Max normalize the parameter points to the [-1.0, 1.0] interval.
(2) Lower threshold: a real number in the range of 0~10.0, the parameter points lower than this value will not participate in the normalization.
(3) Upper threshold: a real number in the range of 0~10.0, the parameter points higher than this value will not participate in the normalization.
(4) Scaling factor: a real number in the range of -1.0~1.0, the normalized parameter value will be multiplied by this value.
(5) Bias: a real number in the range of -1.0~1.0, the normalized and scaled parameter value will be added to this value. This option is used to set the default breath length when the breath mark is converted to a breath parameter. The actual breath length may be less than the default value due to the small gap between notes; some notes may be shortened due to the insertion of breath marks. Setting to 0 or a negative value means ignoring all breath marks. Threshold for splitting Unsupported project version When the distance between notes exceeds the set value, they will be split into different segments (patterns) for subsequent editing. The threshold unit is the value of a quarter note, and the default is 1, which means that when the distance between notes exceeds 1 quarter notes (480 ticks), they will be split. If you don't want to split at all, please set this option to 0 or a negative value. When turned on, the energy envelope will be mapped to the energy channel of the intermediate model. When turned on, the tension envelope will be mapped to the tension channel of the intermediate model. yqzhishen Project-Id-Version:  libresvip
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2024-12-13 18:18+0000
PO-Revision-Date: 2024-11-13 06:38+0000
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: zh_CN
Language-Team: Chinese Simplified
Plural-Forms: nplurals=1; plural=0;
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.16.0
 ACE Studio åæ¶å·æååº¦ä¸å¼ ååæ°ï¼äºèåå¯å½±åæ­å£°çåéæãå¯ä»¥éæ©ååº¦åæ°çæ å°ç®æ ã ACE Studio å·¥ç¨æä»¶ ACE Studio æ¯æä¸å¤§è¯­ç§çæ­è¯ï¼æ¬éé¡¹ç¨äºè®¾å®æ­è¯çè¯­è¨ã ACE Studio ä¼ç»ææçé³ç¬¦æ·»å åé³ãè¿å¯¹äºå¤§é¨åçæ±å­èè¨æ¯ä¸ç§åä½æ°æ®ï¼å æ­¤é»è®¤æåµä¸åªä¼ä¿çè¢«ä¿®æ¹è¿çåé³ãæå¼æ­¤éé¡¹åï¼å°æ æ¡ä»¶ä¿çææçåé³ä¿¡æ¯ï¼ä½å¯è½äº§çæ´å¤§çæä»¶ä½ç§¯ãå½æºæä»¶ä¸­åå«éæ±è¯­æ¼å±æ°æ®æ¶ï¼è¯·å°æ­¤éé¡¹æå¼ã ååº¦ä¸å¼ å æ°å£°å®åæ åååæ° ä¸­æ ACE Studio å·¥ç¨æä»¶è½¬æ¢æä»¶ é»è®¤å¼å¸é¿åº¦ï¼æ¯«ç§ï¼ é»è®¤è¾é³é¿åº¦ (åä½ä¸ºç§) é»è®¤ä½¿ç¨çæ­æ ååº¦å®åæ åååæ° è±è¯­ å¯¼å¥ååº¦åç» å¯¼å¥å¼ ååç» åæ°ç¹éæ ·é´é æ¥è¯­ ä¿çææåé³ä¿¡æ¯ æ­è¯è¯­è¨ å°ååº¦åæ°åæ¶æ å°è³ååº¦ä¸å¼ ååæ°ï¼äºèå°åå  50% çæéã ä»å°ååº¦åæ°æ å°è³ååº¦åæ°ãå¼ ååæ°å°ä¿ææ åã ä»å°ååº¦åæ°æ å°è³å¼ ååæ°ãååº¦åæ°å°ä¿ææ åã å°ååº¦åæ°æ å°è³ ä»ååº¦ ä»å¼ å è¯·è¾å¥å®æ´æ è¯¯çæ­æåå­ã ç»æªè®¾ç½®è¾é³é¿åº¦çé³ç¬¦æ·»å é»è®¤å¼ ç±äº ACE Studio ååº¦åæ°å¯¹é³éçå½±åè¾ä¸ºæ¾èï¼ææä¾æ­¤éé¡¹æ§å¶ååº¦åç»çæ å°ç³»æ°ãååº¦åç»å°è¢«æ´ä½ä¹ä»¥æ­¤éé¡¹çå¼åæ å°å°ä¸­ä»æ¨¡åçé³éééï¼å©ä½çé¨åå°è¢«æ å°å°ååº¦ééãæ­¤éé¡¹æ¥å 0~1.0 èå´åçå¼ã è¥¿ç­çè¯­ ååº¦-é³éæ å°ç³»æ° å¼ åå®åæ åååæ° åä½ä¸ºtickï¼ååé³ç¬¦é¿åº¦ä¸º 480 ticksï¼ãé»è®¤æåµä¸ acep æä»¶ä¸­çåæ°ç¹éç¨éå¸¸å¯éçå­å¨æ¹å¼ï¼éå½æé«éæ ·é´éä¸ä¼é æå¾å¤§çç²¾åº¦æå¤±ï¼ä½å¯ä»¥å¾å°æ´å°çæä»¶ä½ç§¯ãè®¾ç½®ä¸º 0 æè´å¼ä»£è¡¨ä¿æåæéæ ·é´éã æ­¤éé¡¹ä¸ºé«çº§éé¡¹ãå¯ç¨æ­¤éé¡¹åï¼æ°å£°å®åå°ç»è¿æ åååæ¢åä¸æ°å£°åç»åå¹¶ãå»ºè®®ä½¿ç¨åºå®ç¬å·åºå®å¨é¨åæ°ååå¯ç¨æ­¤éé¡¹ãæ­¤éé¡¹éè¦è®¾å® 5 ä¸ªå¼ï¼å½¼æ­¤ä½¿ç¨â,âéå¼ï¼
(1) æ ååæ¹æ³ï¼none ä»£è¡¨å³é­æ­¤éé¡¹ï¼zscore ä»£è¡¨å¯¹åæ°ç¹æ§è¡ Z-Score æ ååï¼minmax ä»£è¡¨å°åæ°ç¹ Min-Max æ ååè³ [-1.0, 1.0] åºé´ã
(2) ä¸éå¼ï¼0~10.0 èå´åçå®æ°ï¼ä½äºæ­¤å¼çåæ°ç¹å°ä¸ä¼åä¸æ ååã
(3) ä¸éå¼ï¼0~10.0 èå´åçå®æ°ï¼é«äºæ­¤å¼çåæ°ç¹å°ä¸ä¼åä¸æ ååã
(4) ç¼©æ¾ç³»æ°ï¼-1.0~1.0 èå´åçå®æ°ï¼æ§è¡æ åååçåæ°å¼å°ä¸æ­¤å¼ç¸ä¹ã
(5) åç½®å¼ï¼-1.0~1.0 èå´åçå®æ°ï¼æ§è¡æ ååå¹¶ç»è¿ç¼©æ¾çåæ°å¼å°ä¸æ­¤å¼ç¸å ã æ­¤éé¡¹ä¸ºé«çº§éé¡¹ãæå¼âå¯¼å¥ååº¦åç»âå¼å³å¹¶å¯ç¨æ­¤éé¡¹åï¼ååº¦å®åå°ç»è¿æ åååæ¢åä¸ååº¦åç»è¿è¡åå¹¶ãå»ºè®®ä½¿ç¨åºå®ç¬å·åºå®å¨é¨åæ°ååå¯ç¨æ­¤éé¡¹ãæ­¤éé¡¹éè¦è®¾å® 5 ä¸ªå¼ï¼å½¼æ­¤ä½¿ç¨â,âéå¼ï¼
(1) æ ååæ¹æ³ï¼none ä»£è¡¨å³é­æ­¤éé¡¹ï¼zscore ä»£è¡¨å¯¹åæ°ç¹æ§è¡ Z-Score æ ååï¼minmax ä»£è¡¨å°åæ°ç¹ Min-Max æ ååè³ [-1.0, 1.0] åºé´ã
(2) ä¸éå¼ï¼0~10.0 èå´åçå®æ°ï¼ä½äºæ­¤å¼çåæ°ç¹å°ä¸ä¼åä¸æ ååã
(3) ä¸éå¼ï¼0~10.0 èå´åçå®æ°ï¼é«äºæ­¤å¼çåæ°ç¹å°ä¸ä¼åä¸æ ååã
(4) ç¼©æ¾ç³»æ°ï¼-1.0~1.0 èå´åçå®æ°ï¼æ§è¡æ åååçåæ°å¼å°ä¸æ­¤å¼ç¸ä¹ã
(5) åç½®å¼ï¼-1.0~1.0 èå´åçå®æ°ï¼æ§è¡æ ååå¹¶ç»è¿ç¼©æ¾çåæ°å¼å°ä¸æ­¤å¼ç¸å ã æ­¤éé¡¹ä¸ºé«çº§éé¡¹ãæå¼âå¯¼å¥å¼ ååç»âå¼å³å¹¶å¯ç¨æ­¤éé¡¹åï¼å¼ åå®åå°ç»è¿æ åååæ¢åä¸å¼ ååç»è¿è¡åå¹¶ãå»ºè®®ä½¿ç¨åºå®ç¬å·åºå®å¨é¨åæ°ååå¯ç¨æ­¤éé¡¹ãæ­¤éé¡¹éè¦è®¾å® 5 ä¸ªå¼ï¼å½¼æ­¤ä½¿ç¨â,âéå¼ï¼
(1) æ ååæ¹æ³ï¼none ä»£è¡¨å³é­æ­¤éé¡¹ï¼zscore ä»£è¡¨å¯¹åæ°ç¹æ§è¡ Z-Score æ ååï¼minmax ä»£è¡¨å°åæ°ç¹ Min-Max æ ååè³ [-1.0, 1.0] åºé´ã
(2) ä¸éå¼ï¼0~10.0 èå´åçå®æ°ï¼ä½äºæ­¤å¼çåæ°ç¹å°ä¸ä¼åä¸æ ååã
(3) ä¸éå¼ï¼0~10.0 èå´åçå®æ°ï¼é«äºæ­¤å¼çåæ°ç¹å°ä¸ä¼åä¸æ ååã
(4) ç¼©æ¾ç³»æ°ï¼-1.0~1.0 èå´åçå®æ°ï¼æ§è¡æ åååçåæ°å¼å°ä¸æ­¤å¼ç¸ä¹ã
(5) åç½®å¼ï¼-1.0~1.0 èå´åçå®æ°ï¼æ§è¡æ ååå¹¶ç»è¿ç¼©æ¾çåæ°å¼å°ä¸æ­¤å¼ç¸å ã æ¬éé¡¹ç¨äºè®¾å®æ¢æ°æ è®°è¢«è½¬æ¢ä¸ºå¼å¸åæ°æ¶é»è®¤çå¼å¸é¿åº¦ãå®éæ¢æ°é¿åº¦å¯è½å é³ç¬¦é´éè¿å°èå°äºé»è®¤å¼ï¼é¨åé³ç¬¦å¯è½éå¼å¸æ è®°çæå¥èç¼©ç­ãè®¾ç½®ä¸º 0 æè´å¼ä»£è¡¨å¿½ç¥æææ¢æ°æ è®°ã çæ®µååéå¼ ä¸æ¯æçå·¥ç¨çæ¬ å½é³ç¬¦ä¹é´çè·ç¦»è¶è¿è®¾å®å¼æ¶ï¼å°è¢«ååè³ä¸åççæ®µï¼patternï¼ä»¥ä¾¿åç»­ç¼è¾ãéå¼åä½ä¸ºååé³ç¬¦æ¶å¼ï¼é»è®¤ä¸º 1ï¼å³å½é³ç¬¦é´è·è¶è¿ 1 ä¸ªååé³ç¬¦æ¶å¼ï¼480 ticksï¼æ¶è¿è¡ååãè¥ä¸å¸æè¿è¡ä»»ä½ååï¼è¯·å°æ­¤éé¡¹è®¾å®ä¸º 0 æè´å¼ã æå¼åï¼å°å¯ä»¥éè¿æ å°æ¯ä¾éé¡¹æ§å¶ååº¦åç»æ å°è³ä¸­ä»æ¨¡åçååº¦ééåé³éééçæ¯ä¾ã æå¼åï¼å¼ ååç»å°è¢«æ å°è³ä¸­ä»æ¨¡åçååº¦ééã YQä¹ç¥ 