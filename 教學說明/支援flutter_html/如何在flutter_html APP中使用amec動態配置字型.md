# 如何在 flutter_html APP 中使用 amec 的動態配置字型

## 場景說明

APP會透由API取得 文章內容(html)及 公用樣式表(CSS)，CSS中會包含font-family，其中會使用到Noto黑體等四種基礎字型，以及其他自託管的特色字型。
由於 APP 使用 flutter_html 無法使用 web 版的字型 js SDK，必須採取 flutter 生態專屬方式。
以下分兩部分說明：基礎字型、特色字型。

## 基礎字型

自託管字型SDK只提供 自託管的特色字型 ，沒有包含作為基礎字型的 Noto 黑體、宋體。
基礎字型的部分請：

- 優先透由官方 google_fonts 套件引用
- 或者，以平台預設同類字型替代。

### 透由官方 google_fonts 套件引用

#### google_fonts 的運作原理：

- 不佔用 APP 體積： 不需要把龐大的思源黑體打包進 APP。
- 首次載入（動態下載）： 當 APP 第一次執行，且畫面上需要顯示該字型時，套件會在背景自動透過 Google 的 API（HTTP 請求）將對應的 .ttf 檔案下載到手機的「本地儲存空間（Local Storage）」。
- 後續載入（快取機制）： 下次使用者打開 APP，套件會發現「手機裡已經有這個字型檔了」，就會直接從手機硬碟讀取，完全不需要再消耗網路流量，速度等同於內建字型。

#### 實作範例

以 amec 網站為例，所引用的基礎字型為：

```html
<link
  id="google-fonts-link"
  href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&family=Noto+Sans+SC:wght@300;400;500;700;900&family=Noto+Serif+TC:wght@300;400;500;700;900&family=Noto+Serif+SC:wght@300;400;500;700;900&display=swap"
  rel="stylesheet"
/>
```

共四套字型，五種字重。
在 Flutter APP 裡，可以直接使用官方的 `google_fonts` 套件，它會自動處理一切底層工作，使用很簡便。

```dart
import 'package:flutter/material.dart';
import 'package:flutter_html/flutter_html.dart';
import 'package:google_fonts/google_fonts.dart';

class ArticleView extends StatelessWidget {
  final String apiHtmlContent; // 從 API 取得的文章 HTML
  final String apiCssContent;  // 從 API 取得的通用樣式表

  const ArticleView({
    Key? key,
    required this.apiHtmlContent,
    required this.apiCssContent,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // 1. 取得 Google Fonts 在系統中動態註冊的真實 Family Name
    final String realNotoSansTc = GoogleFonts.notoSansTc().fontFamily ?? 'Noto Sans TC';
    final String realNotoSerifTc = GoogleFonts.notoSerifTc().fontFamily ?? 'Noto Serif TC';
    final String realNotoSansSc = GoogleFonts.notoSansSc().fontFamily ?? 'Noto Sans SC';
    final String realNotoSerifSc = GoogleFonts.notoSerifSc().fontFamily ?? 'Noto Serif SC';

    // 2. 將 API 傳來的 CSS 進行字串替換
    // 將原本 CSS 寫的 'Noto Sans TC' 替換為 Flutter 真實認得的名稱
    String resolvedCss = apiCssContent
        .replaceAll("'Noto Sans TC'", "'$realNotoSansTc'")
        .replaceAll('"Noto Sans TC"', "'$realNotoSansTc'") // 防呆雙引號
        .replaceAll('Noto Sans TC', "'$realNotoTc'")       // 防呆無引號

        .replaceAll("'Noto Serif TC'", "'$realNotoSerifTc'")
        // ... (其他三種基礎字型依此類推)
        ;

    // 自託管字型 (如 InstrumentSansLatinSubset) 因為會用 FontLoader 自己命名，所以不用替換。

    // 3. 將替換後的 CSS 與 HTML 組合起來
    final String finalHtml = '''
      <html>
        <head>
          <style>
            $resolvedCss
          </style>
        </head>
        <body>
          $apiHtmlContent
        </body>
      </html>
    ''';

    // 4. 交給 flutter_html 渲染
    return Html(
      data: finalHtml,
      // 如果需要針對特殊標籤微調，還是可以在這裡加上 style 屬性
    );
  }
}
```

**關於「字重 (Font-Weight)」的補充：**
不用擔心 CSS 裡的 font-weight: 700; 會失效！flutter_html 在解析 CSS 時，會正確將 font-weight: 700 轉成 Flutter 的 FontWeight.w700。
當 Flutter 文字引擎拿到了正確的 fontFamily 以及對應的 fontWeight，底層的 google_fonts 就會自動去抓取並套用 Noto 粗體的字型檔，完美還原網頁版的樣式！

### 以平台預設同類字型替代

amec 文章所用的「通用樣式表」中，在設定 font-family 時，會將各平台的預設字型作為備援(fallback)，例如(偽代碼)：

```css
一般黑體 {
  font-family:
    InstrumentSansLatinSubset, "Noto Sans TC", "Noto Sans SC", "PingFang TC",
    "Heiti TC", "LiHei Pro", "Microsoft JhengHei", "微軟正黑體",
    "全字庫正宋體 Ext-B", "TW-Sung-Ext-B", sans-serif;
}
一般宋體 {
  font-family:
    "Noto Serif TC", "Noto Serif SC", "Songti TC", PMingLiU, 新細明體, MingLiU,
    細明體, PMingLiU-ExtB, "全字庫正宋體 Ext-B", TW-Sung-Ext-B, serif;
}
楷體 {
  font-family:
    "AR PL UKai TW", "標楷體", "DFKai-SB", "BiauKai", "Kaiti TC",
    "STKaitiTC-Regular", "AR PL KaitiM Big5", "Noto Serif TC",
    "全字庫正楷體 Ext-B", "TW-Kai-Ext-B", serif;
}
仿宋體 {
  font-family:
    "TW-Sung-Punct", "Zhuque Fangsong (technical preview)", "DFPFangSong-W4",
    "華康P仿宋體W4", "DFFangSong-W4", "華康仿宋體W4", "FangSong", "STFangsong",
    "Noto Serif TC", "Source Han Serif TC", "Songti TC", PMingLiU-ExtB,
    "全字庫正宋體 Ext-B", TW-Sung-Ext-B, serif;
}
```

針對這些字體，如果各平台有其它更適當的對映內建字型，可反映以便加入作為備援。

---

## 特色字型(指自託管的部分)

由於無法執行JS，APP端必須自行取得 api\amec.json 字型清單，並參考 github 字型庫的 api\font-loader.js 自行實作邏輯。
在 APP 開發領域，這是一種很常見的架構，通常被稱為「遠端配置（Remote Config）」或是「動態設定檔」。

APP 端實作的工作流程會是這樣：

1. 抓取清單： APP 啟動時，先透過 HTTP 請求去抓取放在 GitHub (或 API 伺服器) 上的 JSON 清單。
2. 解析清單： APP 解析 JSON，得知現在有哪些字型家族（Font-family）、以及對應的 ttf 檔案下載網址。
3. 檢查與下載： APP 檢查手機內部快取是否已經有這些檔案了。如果沒有，才觸發下載。
4. 註冊字型： 使用 FontLoader，將下載來的字型載入記憶體。此時，APP 畫面上的動態字型就會生效。

### 官方 FontLoader

在 Flutter 中，可以使用原生的 FontLoader 類別來實作動態下載與快取。流程如下：

1. 使用 flutter_cache_manager 或自行用 http 下載這個 .ttf 檔案並存在本地的 application document directory。
2. 使用 Flutter 原生的 FontLoader 類別 (final fontLoader = FontLoader('自訂字型名稱');)
3. 將下載好的檔案透過 fontLoader.addFont(位元組資料) 載入。
4. 呼叫 fontLoader.load() 之後，你們的 flutter_html 就可以直接透過 CSS 的 font-family: '自訂字型名稱' 正常渲染出我們的字型了！」

### Flutter 支援的格式有哪些？

Flutter 官方文件明確指出，(flutter_html) 開發 APP 時僅支援以下三種格式：

- .ttf (TrueType) —— 最推薦、最保險
- .otf (OpenType)
- .ttc (TrueType Collection)

### amec.json 字型清單中可供 flutter_html 使用的欄位

amec.json 範例：

```json
[
  {
    "id": "instrument-sans",
    "name": "InstrumentSansLatinSubset",
    "displayName": "Instrument Sans 拉丁子集",
    "cssUrl": "https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/instrument-sans/result.css",
    "ttfUrl": "https://github.com/xiao-xue-seng/fonts/releases/download/app-fonts-v1.0.0/InstrumentSans-Subset.ttf"
  },
  {
    "id": "ukai-cn",
    "name": "AR PL UKai CN",
    "displayName": "AR PL UKai CN",
    "cssUrl": "https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/ukai-cn/result.css",
    "ttfUrl": "https://github.com/xiao-xue-seng/fonts/releases/download/app-fonts-v1.0.0/ukai-cn.ttf"
  }
  // ... 其他字型依此類推
]
```

"name" 是 font-family 中使用的名稱。
"ttfUrl" 即是 APP 所需的字型檔網址。如果缺少此欄位，則表示該字型沒有提供 ttf 檔案。APP 端可使用備援字型呈現。

### APP (Flutter) 的字型整合指南：

由於 Flutter 原生渲染與 flutter_html 不支援直接載入遠端 CSS 與 WOFF2，我們已將 SDK 改為「資料驅動」模式。

#### 步驟 1：取得動態字型清單

請在 APP 啟動時，Fetch 我們的字型 API：
`GET https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/api/amec.json`

#### 步驟 2：解析並下載字型

解析 JSON 後，請提取 name (字型家族名稱) 與 ttfUrl (直連下載點)。
Web 專用的 cssUrl 請直接忽略。

#### 步驟 3：在 Flutter 中實作動態載入

建議的 Flutter 實作邏輯如下（虛擬碼參考）：

```dart
import 'package:http/http.dart' as http;
import 'package:flutter/services.dart'; // 給 FontLoader 用

Future<void> loadDynamicFonts() async {
  // 1. 抓取 JSON 清單
  final response = await http.get(Uri.parse('https://cdn.jsdelivr.net/gh/xiao-xue-seng/fonts@v1/api/amec.json'));
  final List<dynamic> fonts = jsonDecode(response.body);

  for (var font in fonts) {
    final String fontFamilyName = font['name'];
    final String ttfUrl = font['ttfUrl'];

    // 2. 檢查本地快取，若無則下載 TTF 檔案的 ByteData
    // (這裡建議實作本地檔案快取，避免每次打開 APP 都要下載)
    final fontBytes = await fetchAndCacheFont(ttfUrl);

    // 3. 註冊字型到 Flutter 系統中
    final fontLoader = FontLoader(fontFamilyName);
    fontLoader.addFont(Future.value(ByteData.view(fontBytes.buffer)));
    await fontLoader.load();
  }
}
```

在 Flutter 中，要實作這個 fetchAndCacheFont 函數，業界最標準、最省事的做法是使用官方推薦的 flutter_cache_manager 套件。這個套件會全自動處理下載、存檔、快取過期等麻煩事。

```dart
import 'dart:typed_data';
import 'package:flutter/services.dart';
// 需要在 pubspec.yaml 加上這兩個套件：
// flutter_cache_manager: ^3.3.0
// http: ^1.1.0
import 'package:flutter_cache_manager/flutter_cache_manager.dart';

/// 下載並快取字型，回傳 FontLoader 需要的 ByteData
Future<ByteData> fetchAndCacheFont(String fontUrl) async {
  try {
    // DefaultCacheManager 會自動幫我們做這件事：
    // 1. 檢查手機裡有沒有快取過這個網址的檔案
    // 2. 如果沒有，自動發送 HTTP GET 下載並存進手機
    // 3. 如果有，直接回傳手機裡的檔案
    final file = await DefaultCacheManager().getSingleFile(fontUrl);

    // 將實體檔案讀取為位元組陣列 (Uint8List)
    final Uint8List fontBytes = await file.readAsBytes();

    // 轉換成 FontLoader 指定的 ByteData 格式並回傳
    return ByteData.view(fontBytes.buffer);

  } catch (e) {
    print('字型下載或快取失敗: $e');
    throw Exception('Failed to load font from $fontUrl');
  }
}

/// 搭配之前提到的 FontLoader 使用方式：
Future<void> loadCustomFont(String familyName, String url) async {
  final fontLoader = FontLoader(familyName);
  // 呼叫我們實作的下載快取函數
  final fontData = fetchAndCacheFont(url);
  fontLoader.addFont(fontData);
  await fontLoader.load();
}
```

依專案實際情況整合一下，只要完成上述邏輯， flutter_html 在解析 HTML 時，只要遇到 style="font-family: 'AR PL UKai CN'"，就能完美對應並渲染出我們自託管的字型了！

### 效能優化

Q：使用 FontLoader 時，第一次開啟頁面會下載所有字型，需要比較久的時間對嗎？

A： **是的，您的擔心非常有道理！**

如果第一次開啟頁面時，APP 的程式碼寫法是「**把 JSON 清單裡的字型『一次全部排隊下載』**」，那第一次載入確實會需要比較久的時間（特別是中文字型，單一 `.ttf` 檔案動輒 3MB ~ 10MB 以上）。

不過，這個「初次開啟太慢」的問題，**完全可以透過 APP 開發工程師的「載入策略」來解決。**

#### 1. 為什麼第一次會慢？（看程式怎麼寫）

這取決於 APP 怎麼寫那個迴圈：

- ❌ **最糟糕寫法（序列下載 - 慢）：**
  用 `for` 迴圈一個接一個下載。第 1 個下載完才換第 2 個……如果清單有 5 個字型，每個 5MB，總共要下載 25MB，使用者可能要等好幾秒甚至十幾秒。
- ⭕ **普通寫法（並行下載 - 較快）：**
  使用 `Future.wait()` 讓 5 個字型同時平行下載，時間取決於最大的那個檔案。
- 🌟 **最佳寫法（按需載入 / Lazy Loading - 最快）：**
  **文章裡面有用到這個字型，才去下載它！** 沒用到的字型完全不抓。

#### 2. 優化建議

##### 建議一：實作「按需載入（Lazy Loading）」

> **「請不要在頁面一開啟時，就把 `amec.json` 裡的所有字型全部下載。」**
>
> 請先解析當前文章的 HTML/CSS，檢查這篇文章**實際上用了哪幾個 `font-family`**。如果這篇文章只用了《朱雀仿宋》，那就只下載《朱雀仿宋》的 `.ttf`，其他 6 個沒用到的字型完全不要動。這樣可以省下 80% 以上的流量與時間！

##### 建議二：採用「並行下載（Parallel Download）」

> 如果一篇文章剛好用了 2~3 個字型，請使用 Dart 的 `Future.wait()` 進行並行下載，不要用傳統的 `for` 迴圈一個一個排隊下載。
>
> 範例：
>
> ```dart
> // ⭕ 好的做法：同時下載所有需要的字型
> await Future.wait(neededFonts.map((font) => loadCustomFont(font.name, font.ttfUrl)));
> ```

##### 建議三：採「背景載入」，不阻塞畫面（FOUT 模式）

> **「不要讓使用者盯著空白畫面等待下載。」**
>
> APP 可以先用手機預設的字型把文章迅速顯示出來（秒開），同時在背景默默下載需要的 `.ttf`。當 `.ttf` 下載完畢並用 `FontLoader` 註冊後，再刷新畫面切換成美麗的字型。（這就跟網頁的 `font-display: swap` 是一模一樣的體驗！）

#### 3. 第二次開啟會發生什麼事？

只要第一次下載完成並寫入手機快取（Cache）後：

- **第二次開啟同一篇文章：** 0 秒延遲，瞬間讀取本地檔案。
- **開啟另一篇用到相同字型的文章：** 0 秒延遲，因為快取裡面已經有了，不會重複下載。

#### 總結

初次開啟會不會慢，**完全取決於 APP 有沒有做「按需載入（Lazy Loading）」與「並行下載」**。只要「**文章有用到才去抓，不要一次全抓**」，速度就會非常快了！
