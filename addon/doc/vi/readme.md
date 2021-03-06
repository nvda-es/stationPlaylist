# StationPlaylist Studio #

* Tác giả: Geoff Shang, Joseph Lee và các cộng tác viên khác
* Tải về [phiên bản chính thức][1]
* Tải về [phiên bản thử nghiệm][2]
* Tải về [phiên bản hỗ trợ lâu dài][3] - cho người dùng Studio 5.10/5.11

Gói add-on này cung cấp sự cải thiện cho việc sử dụng StationPlaylist
Studio, cũng như cung cấp các tiện ích để điều khiển Studio ở bất cứ đâu.

Để biết thêm thông tin về add-on này, xem [hướng dẫn sử dụng add-on][4]. Với
những người phát triển add-on quan tâm đến việc làm thế nào để tạo add-on,
xem tập tin buildInstructions.txt ở thư mục gốc trong mã nguồn của add-on.

CÁC LƯU Ý QUAN TRỌNG:

* Add-on này yêu cầu NVDA 2018.3 trở lên và StationPlaylist Studio 5.11 trở
  lên.
* Nếu dùng Windows 8 trở lên, hãy tắt chế độ giảm âm thanh để có trải nghiệm
  tốt nhất.
* Từ 2018, [bản ghi những thay đổi cho các bản phát hành cũ của add-on][5]
  sẽ được tìm thấy trên GitHub. Tập tin readme này sẽ liệt kê các thay đổi
  từ phiên bản 5.0 (2015 trở lên).
* Một số tính năng nhất định của add-on (đặc biệt là cập nhật add-on) sẽ
  không hoạt động trong vài điều kiện, bao gồm chạy NVDA trong chế độ bảo
  vệ.
* Vì những giới hạn kĩ thuật, bạn không thể cài hay dùng add-on này với
  phiên bản NVDA từ Windows Store.

## Các phím tắt

Hầu hết chúng chỉ hoạt động trong Studio cho đến khi thực hiện một số thiết
lập khác.

* Alt+Shift+T từ cửa sổ Studio: thông báo thời gian đã trôi qua của track
  đang phát.
* Control+Alt+T (vuốt xuống bằng hai ngón trong chế độ cảm ứng SPL) từ cửa
  sổ Studio: thông báo thời gian còn lại của track đang phát.
* NVDA+Shift+F12 (vuốt lên hai ngón trong chế độ chạm của SPL) từ cửa sổ
  Studio: thông báo thời gian phát thanh như là 5 phút đến đầu giờ. Bấm hai
  lần sẽ thông báo số phút và giây đến đầu giờ.
* Alt+NVDA+1 (vuốt hai ngón tay qua phải trong chế độ SPL) từ cửa sổ Studio:
  mở hộp thoại cài đặt kết thúc track.
* Alt+NVDA+2 (vuốt hai ngón qua trái trong chế độ SPL ) từ cửa sổ Studio: mở
  hộp thoại cài đặt báo động nhạc dạo.
* Alt+NVDA+3 từ cửa sổ Studio: bật tắt cart explorer để tìm hiểu cách gán
  cart.
* Alt+NVDA+4 từ cửa sổ Studio: mở hộp thoại báo động microphone.
* Control+NVDA+f từ cửa sổ Studio: mở hộp thoại để tìm một track theo tên ca
  sĩ hay bài hát. Bấm NvDA+F3 để tìm tiếp hoặc NVDA+Shift+F3 để tìm lùi.
* Alt+NVDA+R từ cửa sổ Studio: chuyển đến các cài đặt thông báo quét thư
  viện.
* Control+Shift+X từ cửa sổ Studio: đi qua các cài đặt hẹn giờ chữ nổi.
* Control+Alt+mũi tên trái phải (khi đứng ở một track trong Studio, Creator,
  và Track Tool): thông báo các cột trước / sau của track.
* Control+Alt+mũi tên lên / xuống (chỉ khi đứng ở tại một track trong
  Studio): chuyển đến track trước hoặc kế và thông báo các cột cụ thể (không
  hỗ trợ cho các add-on phiên bản 15.x).
* Control+NVDA+1 đến 0 (khi đứng ở tại một track trong Studio, Creator và
  Track Tool): thông báo nội dung cho một cột đã định. Bấm hai lần sẽ hiển
  thị thông tin trên cửa sổ duyệt tài liệu.
* Control+NVDA+- (trừ trong Studio): hiển thị dữ liệu của tất cả các cột
  trong một track trên một cửa sổ ở chế độ duyệt.
* Alt+NVDA+C khi đứng tại một track (chỉ trong Studio): thông báo chú thích
  track nếu có.
* Alt+NVDA+0 từ cửa sổ Studio: mở hộp thoại cấu hình add-on của Studio.
* Alt+NVDA+- (trừ) từ cửa sổ Studio: gửi phản hồi cho nhóm phát triển add-on
  bằng trình gửi thư điện tử mặc định.
* Alt+NVDA+F1: mở hộp thoại chào mừng.

## Các lệnh chưa được gán thao tác

Các lệnh sau đây mặc định không được gán thao tác; nếu muốn gán thao tác cho
chúng, hãy dùng hộp thoại quản lý thao tác để thêm lệnh.

* Chuyển đến cửa sổ SPL Studio từ một chương trình bất kì.
* Lệnh cho bộ điều khiển SPL.
* Thông báo trạng thái Studio như track đang phát từ một chương trình bất
  kì.
* SPL Assistant layer từ SPL Studio.
* Thông báo giờ bao gồm giây từ SPL Studio.
* Thông báo nhiệt độ.
* Thông báo tên track kế nếu được lên lịch.
* Thông báo tựa đề của track đang phát.
* Đánh dấu track hiện tại làm track bắt đầu phân tích track theo thời gian.
* Thực hiện phân tích thời gian track.
* Chụp ảnh danh sách phát.
* Tìm kiếm văn bản trong các cột cụ thể.
* Tìm track với  thời lượng trong khoảng thời gian cho trước thông qua tìm
  kiếm theo khoảng thời gian.
* Nhanh chóng bật hay tắt metadata streaming.

## Các lệnh cho thêm khi dùng Sam hay SPL encoders

Các phím lệnh sau  đây hoạt động khi sử dụng Sam hoặc SPL encoders:

* F9: kết nối tới một máy chủ đang phát.
* F10 (chỉ khi dùng SAM encoder): ngắt kết nối khỏi một máy chủ đang phát.
* Control+F9/Control+F10 (chỉ khi dùng SAM encoder): kết nối hay ngắt kết
  nối tất cả các bộ mã hóa.
* F11: bật tắt chế độ để NVDA chuyển đến cửa sổ Studio cho bộ mã hóa được
  chọn nếu đã kết nối.
* Shift+F11: bật tắt chế độ để Studio sẽ phát track đầu tiên được chọn khi
  bộ mã hóa được kết nối đến một máy chủ đang phát.
* Control+F11: bật tắt chế độ theo dõi ngầm của bộ mã hóa được chọn.
* F12: mở một hộp thoại để nhập nhãn tùy chỉnh cho bộ mã hóa hay chương
  trình phát được chọn.
* Control+F12: mở hộp thoại chọn bộ mã hóa đã xóa (sắp xếp lại các cài đặt
  của nhãn phát và các bộ mã hóa).
* Alt+NVDA+0: mở hộp thoại cài đặt mã hóa để cấu hình các tùy chọn như nhãn
  phát.

Ngoài ra, có các lệnh để xem lại cột bao gồm:

* Control+NVDA+1: vị trí mã hóa.
* Control+NVDA+2: nhãn phát thanh.
* Control+NVDA+3 từ SAM Encoder: định dạng mã hóa.
* Control+NVDA+3 từ SPL Encoder: cài đặt mã hóa.
* Control+NvDA+4 từ SAM Encoder: trạng thái kết nối bộ mã hóa.
* Control+NVDA+4 từ SPL Encoder: tốc độ đường truyền hay trạng thái kết nối.
* Control+NVDA+5 từ SAM Encoder: mô tả trạng thái kết nối.

## SPL Assistant layer

Các lệnh này cho phép bạn thu thập nhiều trạng thái khác nhau trên SPL
Studio, như là một track đang phát, thời lượng của tất cả track trong khung
giờ và nhiều nữa. Từ bất cứ cửa sổ SPL Studio nào, bấm các lệnh SPL
Assistant layer rồi bấm một trong các phím trong danh sách dưới đây (một hay
nhiều lệnh chỉ dành riêng cho trình xem danh sách phát). Bạn cũng có thể cấu
hình NvDA để mô phỏng lệnh theo kiểu của các trình đọc màn hình khác.

Các lệnh được hỗ trợ bao gồm:

* A: tự động hóa.
* C (Shift+C trong kiểu phím lệnh của JAWS và Window-Eyes): tên của track
  đang phát.
* C (Kiểu phím lệnh JAWS và Window-Eyes): bật tắt cart explorer (chỉ trong
  trình xem danh sách phát).
* D (R trong kiểu phím lệnh của JAWS): thời lượng còn lại của danh sách phát
  (nếu có thông báo lỗi, di chuyển đến trình xem danh sách phát và thực hiện
  lệnh này).
* `E (G trong kiểu phím lệnh Window-Eyes): trạng thái metadata streaming.
* Shift+1 đến Shift+4, Shift+0: trạng thái của metadata streaming URL cụ thể
  (0 cho DSP encoder).
* E (kiểu phím lệnh của Window-Eyes): thời gian đã phát của track hiện tại.
* F: tìm kiếm track (chỉ  khi ở trong trình xem danh sách phát).
* H: thời lượng phát nhạc của khung giờ hiện tại.
* Shift+H: thời lượng còn lại cho track của khung giờ hiện tại.
* I (L trong kiểu phím lệnh của JAWS hay Window-Eyes): lượt người nghe.
* K: chuyển đến track đã đánh dấu (chỉ khi ở trong trình xem danh sách
  phát).
* Control+K: chọn track hiện tại làm track đánh dấu (chỉ khi ở trong trình
  xem danh sách phát).
* L (Shift+L trong kiểu phím lệnh của JAWS và Window-Eyes): Line in.
* M: Microphone.
* N: tên của track kế được lên lịch.
* P: trạng thái phát nhạc (đang phát hay dừng).
* Shift+P: độ cao của track hiện tại.
* R (Shift+E trong kiểu phím lệnh của JAWS và Window-Eyes): bật / tắt thu ra
  tập tin.
* Shift+R: theo dõi tiến trình quét thư viện.
* S: Track bắt đầu (được lên lịch).
* Shift+S: thời gian đến khi sẽ phát track được chọn (track bắt đầu).
* T: bật / tắt chèn / chỉnh sửa Cart.
* U: Studio tăng thời gian.
* Control+Shift+U: kiểm tra cập nhật add-on.
* W: thời tiết và nhiệt độ nếu được cấu hình.
* Y: trạng thái chỉnh sửa danh sách phát.
* 1 đến 0 (6 cho Studio 5.0x): thông báo nội dung của một cột được chỉ định.
* `F8: lấy ảnh chụp danh sách phát (số track, track dài nhất, v...v....).
* Shift+F8: yêu cầu bảng điểm danh sách phát ở nhiều định dạng.
* F9: đánh dấu track hiện tại là nơi bắt đầu phân tích danh sách phát (chỉ
  khi ở trong trình xem danh sách phát).
* F10: thực hiện phân tích track theo thời gian (chỉ khi ở trong trình xem
  danh sách phát).
* F12: chuyển đổi giữa hồ sơ hiện tại và hồ sơ được chỉ định trước.
* F1: trợ giúp phím lệnh.
* Shift+F1: mở tài liệu hướng dẫn trực tuyến.

## Bộ điều khiển SPL

Bộ điều khiển SPL là tập hợp các lệnh bạn có thể dùng để điều khiển SPL
Studio bất cứ đâu. Bấm các lệnh của bộ điều khiển SPL, và NVDA sẽ đọc, "bộ
điều khiển SPL." Bấm các phím lệnh khác để thực hiện nhiều cài đặt của
Studio như bật / tắt microphone hoặc phát track kế.

Các lệnh của bộ điều khiển SPL bao gồm:

* Bấm P để phát track kế được chọn.
* Bấm U để tạm dừng và tiếp tục phát.
* Bấm S để dừng một track nhỏ dần, hoặc dừng nhanh một track, bấm T.
* Bấm M hay Shift+M để bật / tắt microphone, hoặc bấm N để bật microphone mà
  không có hiệu ứng fade.
* Bấm A để bật tự động hóa hoặc Shift+A để tắt.
* Bấm L để bật đầu vào line-in hoặc Shift+L để tắt.
* Bấm R để biết thời gian còn lại của track đang phát.
* Bấm Shift+R để xem báo cáo về tiến trình quét thư viện.
* Bấm C để NVDA thông báo tên và thời lượng của track đang phát.
* Bấm Shift+C để NVDA thông báo tên và thời lượng của track sắp tới nếu có.
* Bấm E để biết số lượng và các nhãn của các bộ mã hóa đang được theo dõi.
* Bấm I để thu thập số lượng người nghe.
* Bấm Q để thu thập nhiều thông tin trạng thái về Studio bao gồm việc có một
  track đang phát, microphone đang bật và các thông tin khác.
* Bấm các phím cart (ví dụ F1, Control+1) để phát cart được gán từ bất cứ
  đâu.
* Bấm H để hiện hộp thoại trợ giúp với toàn bộ các lệnh được liệt kê.

## Các báo động cho track

Mặc định, NvDA sẽ phát tiếng beep nếu track còn lại five giây (còn lại ở
cuối track) hoặc đầu track. Để thiết lập giá trị này hoặc bật / tắt chúng,
bấm Alt+NVDA+1 hoặc Alt+NVDA+2 mở hộp thoại end of track và song ramp. Ngoài
ra, dùng hộp thoại cài đặt add-on của Studio để thiết lập nếu nghe thấy
tiếng beep, thấy một thống điệp hoặc cả hai when khi bật báo động.

## Các báo động cho microphone

Bạn có thể yêu cầu NVDA phát âm thanh khi microphone đã hoạt động được một
thời gian ngắn. Bấm Alt+NVDA+4 để cấu hình thời gian báo động bằng giây (0
để tắt).

## Tìm kiếm track

Nếu muốn nhanh chóng tìm kiếm một bài hát theo tên hay theo ca sĩ, từ danh
sách track, bấm Control+NVDA+F. Nhập hoặc chọn tên ca sỉ hay tên bài
hát. NVDA sẽ đưa bạn đến bài hát nếu tìm thấy hoặc hiển thị thông báo lỗi
nếu không tìm thấy bài hát đó. Để tìm lại bài hát hay ca sĩ đã tìm trước đó,
bấm NVDA+F3 hoặc NVDA+Shift+F3 để tìm tiếp hay tìm lùi.

Lưu ý: tìm kiếm track có phân biệt chữ hoa / thường.

## Khám phá cart

Tùy vào phiên bản, SPL Studio cho phép gán đến 96 cart cho việc phát
thanh. NVDA cho phép bạn nghe để biết cart, hay tiếng chuông nào được gán
cho các  lệnh này.

Để xem các  cart được gán, từ SPL Studio, bấm Alt+NVDA+3. Bấm lệnh của cart
một lần sẽ cho biết tiếng chuông nào được gán cho lệnh đó. Bấm hai lần sẽ
phát tiếng chuông. Bấm Alt+NvDA+3 để thoát cart explorer. Xem hướng dẫn sử
dụng add-on để biết thêm thông tin về cart explorer.

## Phân tích thời gian track

Để biết tổng thời lượng phát các track được chọn, đánh dấu track hiện tại
làm điểm bắt đầu phân tích thời gian track (SPL Assistant, F9), rồi bấm SPL
Assistant, F10 khi kết thúc vùng chọn.

## Khám phá các cột

Bấm Control+NVDA+1 đến 0 hoặc SPL Assistant, 1 đến 0, bạn có thể thu thập
các nội dung của các cột cụ thể. Mặc định là ca sĩ, tựa đề, thời lượng, nhạc
dạo, loại, tên tập tin, năm, album, thể loại và thời gian được lên lịch. Bạn
có thể cấu hình những cột nào sẽ được khám phá thông qua hộp thoại khám phá
cột được tìm thấy trong hộp thoại cài đặt add-on.

## Ảnh chụp danh sách phát

Bạn có thể bấm SPL Assistant, F8 khi đứng ở tại một danh sách phát trong
Studio để thu thập nhiều thông tin thống kê về danh sách phát đó, bao gồm số
track trong danh sách phát, track dài nhất, ca sĩ tiêu biểu và nhiều
nữa. Sau khi gán một lệnh tùy chỉnh cho tính năng này, bấm phím lệnh đó hai
lần để NVDA trình bày thông tin ảnh chụp của danh sách phát như một trang
web và bạn có thể dùng chế độ duyệt để di chuyển (bấm escape để đóng).

## Bảng điểm của danh sách phát

Bấm SPL Assistant, Shift+F8 sẽ mở một hộp thoại cho phép bạn yêu cầu bảng
điểm của danh sách phát ở nhiều định dạng, bao gồm văn bản thô, bảng HTML
hoặc một danh sách.

## Hộp thoại cấu hình

Từ cửa sổ studio, bạn có thể bấm Alt+NVDA+0 để mở hộp thoại cấu hình
add-on. Cách khác, vào trình đơn tùy chỉnh của NVDA và chọn mục Cài đặt SPL
Studio. Hộp thoại này cũng dùng để quản lý các hồ sơ phát thanh.

## Chế độ chạm của SPL

Nếu dùng Studio trên một máy tính cảm ứng chạy Windows 8 trở lên và cài đặt
NVDA 2012.3 trở lên, bạn có thể thực hiện vài lệnh của Studio từ mành hình
cảm ứng. Trước tiên, dùng thao tác chạm ba ngón để chuyển sang chế độ SPL,
và sử dụng các thao tác cảm ứng đã liệt kê ở trên để thực hiện các lệnh.

## Phiên bản 18.11/18.09.5-LTS

Lưu ý: 18.11.1 thay thế 18.11 để cung cấp những hỗ trợ đắc lực hơn cho
Studio 5.31.

* Bắt đầu hỗ trợ cho StationPlaylist Studio 5.31.
* Giờ bạn có thể thu thập các ảnh chụp (SPL Assistant, F8) và bảng điểm danh
  sách phát (SPL Assistant, Shift+F8) khi một danh sách phát được mở nhưng
  con trỏ không đứng ở tack đầu tiên.
* NVDA sẽ không còn tình trạng không làm gì hoặc phát âm thanh báo lỗi khi
  cố gắng thông báo trạng thái metadata streaming khi khởi độn Studio nếu đã
  được cấu hình như vậy.
* Nếu được cấu hình để thông báo trạng thái metadata streaming khi khởi động
  Studio, việc thông báo trạng thái metadata streaming sẽ không còn bỏ đi
  các thông báo thay đổi thanh trạng thái và ngược lại.

## Phiên bản 18.10.2/18.09.4-LTS

* Sửa lỗi không đóng được màn hình cài đặt add-on nếu đã bấm nút Áp dụng và
  và sau đó lại bấm nút Đồng ý hay Hủy.

## Phiên bản 18.10.1/18.09.3-LTS

* Giải quyết vài trục trặc liên quan đến tính năng thông báo kết nối bộ mã
  hóa, bao gồm việc không thông báo thông điệp trạng thái, không phát track
  đầu tiên được chọn hoặc không chuyển đến cửa sổ Studio khi đã kết
  nối. Những lỗi này gây ra bởi wxPython 4 (NVDA 2018.3 trở lên).

## Phiên bản 18.10

* Yêu cầu NVDA 2018.3 trở lên.
* Những thay đổi bên trong để add-on tương thích hơn với Python 3.

## Phiên bản 18.09.1-LTS

* Khi lấy thông tin bảng điểm danh sách phát ở định dạng bảng HTML, Các tiêu
  đề cột không còn bị chuyển thành dạng giống danh sách chuỗi của Python.

## Phiên bản 18.09-LTS

Phiên bản 18.09.x là loạt phát hành cuối cùng hỗ trợ Studio 5.10 và dựa trên
các công nghệ cũ, với 18.10 trở lên hỗ trợ Studio 5.11/5.20 và các tính năng
mới. Vài tính năng mới sẽ hỗ trợ ngược trở lại 18.09.x nếu cần.

* Khuyến khích dùng NVDA 2018.3 trở lên vì sử dụng wxPython 4.
* Màn hình cài đặt Add-on giờ đây đã hiển thị trên giao diện nhiều trang bắt
  nguồn từ NVDA 2018.2 trở lên.
* Test Drive Fast và Slow rings đã được gom lại thành kênh "development"
  (thử nghiệm), với tùy chọn cho người dùng các bản đang phát triển kiểm tra
  các tính năng thử nghiệm bằng cách chọn vào hộp kiểm các tính năng thử
  nghiệm trong cài đặt nâng cao của add-on. Người dùng ở kênh Test Drive
  Fast ring sẽ tiếp tục kiểm tra các tính năng thử nghiệm.
* Đã gỡ bỏ tính năng chọn các kênh  cập nhật add-on khác nhau từ cài đặt
  add-on. Người dùng muốn chuyển sang kênh phát hành khác phải vào trang
  cộng đồng NVDA add-on (addons.nvda-project.org), chọn StationPlaylist
  Studio rồi tải bản phát hành mong muốn.
* Các dấu kiểm để bao gồm cột cho việc thông báo cột và bảng điểm danh sách
  phát, kể cả các hộp kiểm cho metadata streams cũng đã được chuyển sang
  dạng checkable (tạm dịch: có thể chọn).
* Khi chuyển qua lại giữa các bản cài đặt, NvDA sẽ nhớ các thiết lập hiện
  tại cho các cài đặt hồ sơ cụ thể (báo động, thông báo cột, cài đặt cho
  metadata streaming ).
* Thêm định dạng CSV (dùng dấu phẩy ngăn cách các giá trị) như một định dạng
  cho bảng điểm của danh sách phát.
* Bấm Control+NvDA+C để lưu thiết lập sẽ lưu luôn thiết lập của Studio
  add-on (yêu cầu NVDA 2018.3).

## Phiên bản 18.08.2

* NVDA sẽ không kiểm tra cập nhật Studio add-on nếu đã cài Add-on
  Updater. Hậu quả là cài đặt add-on sẽ không còn bao gồm các thiết lập liên
  quan đến cập nhật add-on trong trường hợp này. Nếu đang sử dụng Add-on
  Updater, bạn nên dùng tính năng của add-on này để kiểm tra cập nhật Studio
  add-on.

## Phiên bản 18.08.1

* Sửa lỗi khác của wxPython 4 liên quan đến tính tương thích xảy ra khi
  thoát Studio.
* NVDA sẽ thông báo một thông điệp thích hợp khi không hiển thị được các văn
  bản chỉnh sửa của danh sách phát, thường thấy sau khi mở một danh sách
  phát chưa chỉnh sửa hoặc khi khởi động Studio.
* NVDA sẽ không còn tình trạng không làm gì hoặc phát âm thanh báo lỗi khi
  cố gắng thu thập trạng thái metadata streaming thông qua SPL Assistant
  (E).

## Phiên bản 18.08

* Hộp thoại cài đặt Add-on giờ đây đã dùng giao diện cài đặt nhiều nhánh tìm
  thấy trong NVDA 2018.2. Vậy nên, bản phát hành này yêu cầu NVDA 2018.2 trở
  lên. Giao diện cài đặt cũ của add-on không còn được dùng nữa và sẽ bị gỡ
  bỏ trong năm 2018.
* Đã thêm một phần mới (nút / bảng) trong cài đặt add-on để cấu hình các tùy
  chỉnh cho bảng điểm danh sách phát, được dùng để cấu hình việc bao gồm và
  sắp xếp các cột cho tính năng này cũng như các cài đặt khác.
* Khi tạo một bảng theo điểm của danh sách phát và nếu có thực hiện tùy
  chỉnh sắp xếp hay xóa cột, NVDA sẽ dùng tùy chỉnh trình bày sắp xếp cột đã
  thiết lập từ cài đặt add-on hoặc không bao gồm thông tin từ các cột đã
  xóa.
* Khi dùng các lệnh điều hướng cột trong các mục của track
  (Control+Alt+home/end/mũi tên trái/mũi tên phải) trong Studio, Creator và
  Track Tool, NVDA sẽ không còn tình trạng thông báo sai cột dữ liệu sau khi
  thay đổi vị trí cột trên màn hình bằng chuột.
* Những cải thiện đáng kể đến các phản hồi của NVDA khi dùng các lệnh điều
  hướng cột trong Creator và Track Tool. Cụ thể, khi dùng Creator, NVDA sẽ
  phản hồi tốt hơn khi dùng các lệnh điều hướng cột.
* NVDA sẽ không còn tịnh trạng phát âm thanh báo lỗi hoặc không làm gì khi
  nỗ lực thêm các chú thích vào track trong Studio hay khi thoát NVDA trong
  lúc đang sử dụng Studio, lỗi gây ra bởi vấn đề tương thích của wxPython 4.

## Phiên bản 18.07

* Thêm vào màn hình cài đặt add-on nhiều nhánh để thử nghiệm, tiếp cận bằng
  cách bật / tắt một thiết lập trong cài đặt add-on / hộp thoại nâng cao
  (cần phải khởi động lại NVDA sau khi cấu hình để hiện hộp thoại mới). Tính
  năng này dành cho nguiờ dùng NVDA 2018.2, và không phải tất cả các cài đặt
  của add-on đều có thể cấu hình ở đây.
* NVDA sẽ không còn tình trạng phát âm thanh báo lỗi hoặc không làm gì khi
  nỗ lực đổi tên một hồ sơ phát thanh từ cài đặt add-on, lỗi gây ra bởi vấn
  đề tương thích của wxPython 4.
* Khởi động lại NvDA hoặc Studio sau khi thực hiện các thay đổi trong cài
  đặt của một hồ sơ phát thanh không phải hồ sơ bình thường, NVDA sẽ không
  còn tình trạng trở về các cài đặt cũ.
* Đã có thể  thu thập bảng điểm của danh sách phát cho khung giờ hiện
  tại. Chọn "khung giờ hiện tại" trong các tùy chọn khoảng danh sách phát
  trong bảng điểm của danh sách phát (SPL Assistant, Shift+F8).
* Thêm một tùy chọn trong hộp thoại bảng điểm của danh sách phát để lưu điểm
  thành một tập tin (tất cả định dạng) hoặc chép vào bộ nhớ tạm (chỉ văn bản
  thô và định dạng bảng Markdown) thêm nữa là hiện điểm ra màn hình. Khi lưu
  bảng điểm, chúng ở tại thư mục Documents của người dùng, trong thư mục
  "nvdasplPlaylistTranscripts".
* Trạng thái cột không còn được bao gồm khi tạo bảng điểm của danh sách phát
  ở định dạng HTML và Markdown.
* Khi đứng ở tại một track trong Creator và Track Tool, bấm Control+NVDA+các
  phím số hai lần sẽ trình bày các cột thông tin trên một cửa sổ ở chế độ
  duyệt.
* Trong Creator và Track Tool, đã thêm các phím Control+Alt+Home/End để di
  chuyển đến cột đầu hay cuối cho track tại vị trí con trỏ.

## Phiên bản  18.06.1

* Sửa vài lỗi tương thích với wxPython 4, bao gồm lỗi mở các hộp thoại tìm
  kiếm track (Control+NVDA+F), tìm kiếm cột và tìm kiếm theo khoảng thời
  gian trong Studio và hộp thoại tạo nhãn phát thanh (F12) từ cửa sổ các bộ
  mã hóa.
* Khi mở một hộp thoại tìm kiếm từ Studio và xảy ra lỗi không mong muốn,
  NVDA sẽ trình bày thêm các thông điệp hợp lý thay vì chỉ nói rằng một hộp
  thoại tìm kiếm khác đang mở.
* Trong cửa sổ của các bộ mã hóa, NVDA sẽ không còn phát âm tanh báo lỗi
  hoặc không làm gì khi nỗ lực mở hộp thoại cài đặt mã hóa (Alt+NVDA+0).

## Phiên bản 18.06

* Trong hộp thoại cài đặt add-on, thêm nút "Áp dụng" để có thể áp dụng các
  thay đổi cho hồ sơ hiện tại mà không đóng hộp thoại. Tính năng này hoạt
  động với NVDA 2018.2.
* Khắc phục lỗi NVDA áp dụng các thay đổi cho cài đặt khám phá cột mặc dù
  bấm nút hủy từ hộp thoại cài đặt add-on.
* Trong Studio, bấm Control+NVDA+phím số hai lần khi đứng tại một track để
  hiển thị thông tin cho một cột cụ thể trên một cửa sổ chế độ duyệt.
* Khi đứng ở một track trong Studio, bấm Control+NVDA+trừ sẽ hiển thị dữ
  liệu của tất cả các cột trên một cửa sổ chế độ duyệt.
* Trong StationPlaylist Creator, khi đứng ở một track, bấm Control+NVDA+phím
  số sẽ thông báo dữ liệu cho một cột cụ thể.
* Thêm một nút trong hộp thoại cài đặt Studio add-on để cấu hình khám phá
  các cột cho SPL Creator.
* Thêm định dạng Markdown như một định dạng cho bảng điểm của danh sách
  phát.
* Phím lệnh gửi thư điện tử cho nhóm phát triển đã được đổi từ
  Control+NVDA+trừ thành Alt+NVDA+trừ.

## Phiên bản 18.05

* Thêm khả năng chụp nhanh một phần ảnh của danh sách phát. Có thể làm điều
  này bằng cách chỉ định khoảng phân tích (SPL Assistant, F9 ở điểm bắt đầu
  của khoảng cần phân tích) và chuyển một mục khác rồi thực hiện lệnh chụp
  ảnh danh sách phát.
* Thêm một lệnh mới trong SPL Assistant để yêu cầu bảng điểm của danh sách
  phát ở một số định dạng (Shift+F8). Chúng bao gồm văn bản thô, bảng HTML
  hay danh sách HTML.
* Nhiều tính năng phân tích danh sách phát như phân tích track theo thời
  gian và ảnh chụp danh sách phát giờ đây được liệt kê trong giao diện của
  "Trình phân tích danh sách phát".

## Phiên bản 18.04.1

* NVDA sẽ không còn bị lỗi khi đếm ngược đến giờ hẹn cho một hồ sơ phát theo
  thời gian nếu NVDA được cài đặt và dùng với wxPython 4 toolkit.

## Phiên bản 18.04

* Đã thực hiện các thay đổi để tính năng kiểm tra cập nhật add-on trở nên
  đáng tin cậy hơn, cụ thể là khi bật tính năng tự kiểm tra cập nhật.
* NVDA sẽ phát một âm thanh để biểu thị việc bắt đầu quét thư viện khi nó
  được cấu hình phát tiếng beep cho các thông báo khác nhau.
* NVDA sẽ bắt đầu ngầm quét thư viện nếu nó được bắt đầu từ các hộp thoại
  tùy chọn của Studio hoặc bắt đầu khi khởi động.
* Chạm hai lần vào track trên màn hình cảm ứng hoặc thực hiện các lệnh mặc
  định sẽ chọn track và chuyển con trỏ hệ thống đến nó.
* Khi chụp ảnh của danh sách phát (SPL Assistant, F8), nếu một danh sách
  phát chỉ bao gồm các điểm đánh dấu theo giờ, sửa vài lỗi làm cho NVDA
  không thực hiện chụp ảnh.

## Phiên bản 18.03/15.14-LTS

* Nếu được cấu hình để thông báo trạng thái metadata streaming khi khởi động
  Studio, NVDA sẽ tôn trọng thiết lập này và không thông báo trạng thái phát
  khi chuyển đến và chuyển đi khỏi các hồ sơ chuyển nhánh.
* Nếu chuyển đến hay chuyển đi khỏi một hồ sơ chuyển nhanh, và NVDA được cấu
  hình thông báo trạng thái metadata streaming khi nó xuất hiện, NVDA sẽ
  không còn đọc thông tin này nhiều lần khi chuyển nhanh đến các hồ sơ.
* NVDA sẽ nhớ chuyển đến các hồ sơ theo thời gian thích hợp (nếu chỉ định
  cho một chương trình) sau khi khởi động lại NVDA nhiều lần trong chương
  trình phát thanh.
* Nếu một hồ sơ theo thời gian có thời lượng hoạt động đang chạy và khi hộp
  thoại cài đặt add-on được mở hay đóng, NVDA vẫn sẽ chuyển trở về hồ sơ
  nguyên thủy khi kết thúc hồ sơ theo thời gian.
* Nếu một hồ sơ theo thời gian được kích hoạt (cụ thể là trong lúc phát
  thanh), sẽ không thay đổi được tác nhân hồ sơ phát thanh thông qua hộp
  thoại cài đặt ađd-on.

## Phiên bản 18.02/15.13-LTS

* 18.02: do các thay đổi bên trong để hỗ trợ các tính năng mở rộng nên yêu
  cầu NVDA 2017.4.
* Việc cập nhật add-on sẽ không thực hiện được trong vài trường hợp bao gồm
  chạy NVDA từ mã nguồn hay chế độ bảo vệ đang bật. Việc kiểm tra chế độ bảo
  vệ cũng áp dụng cho 15.13-LTS.
* Nếu có lỗi xảy ra khi kiểm tra cập nhật, chúng sẽ được ghi lại và NVDA sẽ
  gợi ý bạn đọc nó để biết thêm chi tiết.
* Trong cài đặt add-on, nhiều cài đặt cập nhật trong phần cài đặt nâng cao
  như cập nhật theo thời gian sẽ không hiển thị nếu không được hỗ trợ cập
  nhật add-on.
* NVDA sẽ không còn tình trạng bị đóng băng hoặc không làm gì khi chuyển đến
  một hồ sơ chuyển nhanh hay hồ sơ theo thời gian và NVDA được cấu hình để
  thông báo trạng thái metadata streaming.

## Phiên bản 18.01/15.12-LTS

* Khi dùng kiểu phím lệnh của JAWS cho SPL Assistant, lệnh kiểm tra cập nhật
  (Control+Shift+U) đã làm việc chính xác.
* Khi thay đổi cài đặt báo động cho microphone thông qua hộp thoại báo động
  (Alt+NVDA+4), các thay đổi như bật báo động và thay đổi của báo động
  microphone theo giờ được áp dụng khi đóng hộp thoại.

## Phiên bản 17.12

* Yêu cầu Windows 7 Service Pack 1 trở lên.
* Vài tính năng của add-on đã được cải thiện. Điều này cho phép báo động
  microphone và metadata streaming phản hồi đến các thay đổi trong hồ sơ
  phát thanh. Yêu cầu NvDA 2017.4.
* Khi thoát Studio, nhiều hộp thoại của add-on như cài đặt add-on, hộp thoại
  báo động và nhiều nữa sẽ tự đóng lại. Yêu cầu NVDA 2017.4.
* Thêm một lệnh mới trong bộ điều khiển SPL để thông báo tên của track sắp
  tới nếu có (Shift+C).
* Giờ bạn có thể bấm các phím của cart (ví dụ như F1) sau khi vào bộ điều
  khiển SPl để phát các cart được gán ở bất cứ đâu.
* Do các thay đổi có trong wxPython 4 GUI toolkit, hộp thoại xóa nhãn phát
  thanh giờ đây là một hộp xổ thay vì là một trường nhập số.

## Phiên bản 17.11.2

Đây là phiên bản chính thức cuối cùng  còn hỗ trợ Windows XP, Vista và 7
không có Service Pack 1. Phiên bản sắp tới cho các hệ điều hành này sẽ là
bản phát hành 15.x LTS.

* Nếu dùng các bản phát hành Windows trước Windows 7 Service Pack 1, bạn
  không thể chuyển sang kênh thử nghiệm.

## Phiên bản 17.11.1/15.11-LTS

* NVDA sẽ không còn phát âm thanh báo lỗi hoặc không làm gì khi dùng các
  phím Control+Alt+mũi tên trái phải để điều hướng qua các cột trong Track
  Tool 5.20 với một track đã mở. Thay đổi này yêu cầu Studio 5.20, build 48
  trở lên.

## Phiên bản 17.11/15.10-LTS

* Bắt đầu hỗ trợ cho StationPlaylist Studio 5.30.
* Nếu báo động microphone hay báo giờ theo thời gian được bật, và nếu thoát
  Studio trong khi còn bật microphone, NVDA sẽ không còn phát âm báo động
  microphone từ mọi cửa sổ.
* Khi xóa các hồ sơ phát thanh và nếu một hồ sơ khác trở thành hồ sơ chuyển
  nhanh, cờ báo chuyển nhanh sẽ không bị gỡ khỏi hồ sơ chuyển.
* Nếu xóa một hồ sơ đang hoạt động mà không phải hồ sơ chuyển nhánh hay theo
  thời gian, NVDA sẽ hỏi một lần nữa để xác nhận trước khi thực hiện.
* NVDA sẽ áp dụng chính xác các cài đặt cho báo động microphone khi chuyển
  sang các hồ sơ thông qua hộp thoại cài đặt add-on.
* Giờ bạn có thể bấm SPL Controller, H để xem thông tin giúp đỡ cho bộ điều
  khiển SPL.

## Phiên bản 17.10

* Nếu dùng các bản phát hành Windows trước Windows 7 Service Pack 1, bạn
  không thể chuyển sang kênh cập nhật Test Drive Fast. Một bản phát hành
  trong tương lai của add-on này sẽ chuyển những người dùng các phiên bản
  Windows cũ sang một kênh hỗ trợ riêng.
* Vài cài đặt chung như tiếng beep thông báo trạng thái, thông báo về đầu
  hay cuối danh sách phát và nhiều nữa giờ đây đã được lưu tại hộp thoại cài
  đặt add-on mới (truy cập từ một nút mới trong cài đặt add-on).
* Giờ đã có thể gán thuộc tính chỉ đọc (read-only) cho các tùy chọn của
  add-on, chỉ cần dùng hồ sơ bình thường, hoặc không gọi các cài đặt từ ổ
  đĩa khi khởi động Studio. Những điều này được điều khiển bởi một lệnh
  chuyển mới dành riêng cho add-on này.
* Khi chạy NVDA từ hộp thoại Run (Windows+R), bạn có thể dùng thêm các dòng
  lệnh chuyển để thay đổi cách hoạt động của add-on. Chúng bao gồm
  "--spl-configvolatile" (thuộc tính chỉ đọc cho các cài đặt),
  "--spl-configinmemory" (không gọi các cài đặt từ ổ đĩa), và
  "--spl-normalprofileonly" (chỉ dùng hồ sơ bình thường).
* Nếu thoát Studio (nhưng không thoát NVDA) khi một hồ sơ chuyển nhanh đang
  hoạt động, NVDA sẽ không còn đưa ra thông báo gây hiểu lầm khi chuyển đến
  một hồ sơ chuyển nhanh khi dùng lại Studio.

## Phiên bản 17.09.1

* Như là kết quả của một thông báo từ NV Access rằng NVDA 2017.3 sẽ là phiên
  bản cuối cùng hỗ trợ các phiên bản Windows trước windows 7 Service Pack 1,
  Studio add-on sẽ hiện một thông điệp nhắc nhớ chuyện này nếu chạy từ các
  bản phát hành Windows cũ. Ngưng hỗ trợ cho các bản phát hành Windows cũ từ
  add-on này (thông qua bản phát hành hỗ trợ dài hạn) được lên lịch cho
  tháng tư 2018.
* NVDA sẽ không còn hiện hộp thoại startup hoặc thông báo phiên bản Studio
  nếu được chạy với lệnh chuyển minimal (nvda -rm). Chỉ ngoại lệ cho hộp
  thoại các bản phát hành Windows cũ.

## Phiên bản 17.09

* Nếu người dùng mở hộp thoại tùy chọn nâng cao của add-on khi kênh cập nhật
  và thời gian cập nhật được thiết lập là Test Drive Fast và 0 ngày, NVDA sẽ
  không hiện thông điệp cảnh báo cho kênh cập nhật và thiờ gian cập nhật khi
  thoát hộp thoại.
* Lệnh cho phần còn lại của danh sách phát và phân tích track theo thời gian
  giờ đây yêu cầu một danh sách phát được mở. Nếu không, sẽ hiện thông báo
  lỗi.

## Phiên bản 17.08.1

* NVDA sẽ không còn bị lỗi khiến cho Studio phát track đầu tiên khi kết nối
  bộ mã hóa.

## Phiên bản 17.08

* Các thay đổi về kênh cập nhật: try build giờ đổi thành Test Drive Fast,
  development channel đổi thành Test Drive Slow. True "try" builds sẽ được
  bảo lưu cho các bản dùng thử có yêu cầu người dùng phải cài đặt thủ công.
* Giờ đây, đã có thể thiết lập thời gian cập nhật là 0 ngày. Điều này cho
  phép add-on kiểm tra cập nhật khi khởi động NVDA hay SPL Studio. Sẽ có một
  yêu cầu xác nhận việc chọn thời gian cập nhật là 0 ngày.
* NVDA sẽ không còn tình trạng lỗi kiểm tra cập nhật add-on nếu cập nhật
  theo thời gian được thiết lập là 25 ngày trở lên.
* Trong cài đặt add-on, thêm hộp kiểm để NvDA phát âm thanh khi xuất hiện
  yêu cầu của người nghe. Để dùng tính năng này, cửa sổ yêu cầu phải hiển
  thị khi có yêu cầu.
* Bấm lệnh xem thời gian phát thanh (NVDA+Shift+F12) hai lần sẽ làm cho NVDA
  thông báo giờ và phút còn lại trong khung giờ hiện tại.
* Giờ đã có thể dùng lệnh  tìm kiếm track (Control+NVDA+F) để tìm tên các
  track đã tìm trước đó bằng cách chọn một cụm từ tìm kiếm trong lịch sử từ
  đã nhập.
* Khi thông báo tên track hiện tại và track kế qua SPL Assistant, giờ đã có
  thể bao gồm các thông tin về việc Studio nội bộ nào sẽ phát track.
* Thêm một thiết lập trong cài đặt add-on ở phần thông báo trạng thái để bao
  gồm thông tin phát khi thông báo tựa đề của track hiện tại và track kế.
* Sửa lỗi trong hộp thoại gợi ý tạm cũng như các hộp thoại khác khiến NVDA
  không thông báo các giá trị mới khi thao tác với bộ chọn thời gian.
* NVDA có thể ngăn chặn việc thông báo tiêu đề cột như ca sĩ và phân loại
  khi xem lại track trong trình xem danh sách phát. Đây là thiết lập cho một
  hồ sơ phát thanh riêng biệt.
* Thêm một hộp kiểm trong hộp thoại cài đặt add-on để ngăn chặn thông báo
  các tiêu đề cột khi xem lại track trong trình xem danh sách phát.
* Thêm một lệnh trong bộ điều khiển SPL để thông báo tên và thời lượng của
  track đang phát từ bất cứ đâu (C).
* Khi thu thập các thông tin trạng thái thông qua bộ điều khiển SPL (Q)
  trong khi dùng Studio 5.1x, các thông tin như trạng thái microphone, chế
  độ chỉnh sửa cart và các thông tin khác cũng được thông báo ngoài phát lại
  và tự động hóa.

## Phiên bản 17.06

* Giờ bạn có thể thực hiện lệnh tìm kiếm track (Control+NVDA+F) khi đã tải
  một danh sách phát nhưng con trỏ không đứng ở track đầu tiên.
* NVDA sẽ không còn phát âm thanh báo lỗi hoặc không làm gì khi tìm kiếm một
  track tiếp theo từ track cuối hay track trước từ track đầu tiên.
* Bấm NVDA+Delete bàn phím số (NVDA+Delete với kiểu bàn phím laptop) giờ đây
  sẽ thông báo vị trí track và số thứ tự của mục đó trong một danh sách
  phát.

## Phiên bản 17.05.1

* NVDA sẽ không còn bị lỗi khi lưu các thay đổi cho cài đặt báo động từ
  nhiều hộp thoại báo động (ví dụ, Alt+NVDA+1 cho báo động cuối track).

## Phiên bản 17.05/15.7-LTS

* Giờ đây, thời gian cập nhật có thể thiết lập là 180 ngày. Mặc định, thời
  gian kiểm tra cập nhật là 30 ngày.
* Sửa lỗi NVDA có thể phát âm thanh báo lỗi nếu thoát Studio khi một hồ sơ
  theo thời gian đang hoạt động.

## Phiên bản 17.04

* Đã thêm bản ghi dò lỗi cơ bản cho add-on bằng cách ghi lại nhiều thông tin
  khi add-on hoạt động với chế độ bản ghi dò lỗi của NVDA được bật (yêu cầu
  NVDA 2017.1 trở lên). Để dùng tính năng này, sau khi cài đặt NVDA 2017.1,
  từ hộp thoại thoát NVDA, chọn "Khởi động lại với bản ghi dò lỗi được bật".
* Cải thiện hiển thị cho nhiều hộp thoại của add-on. Cảm ơn tính năng của
  NVDA 2016.4.
* NVDA sẽ ngầm tải cập nhật add-on về  nếu chọn "yes" khi được yêu cầu cập
  nhật add-on. Kết quả là sẽ không hiện thông báo tải tập tin về cỉa các
  trình duyệt web.
* NVDA sẽ không còn tình trạng bị đóng băng khi kiểm tra phiên bản mới lúc
  khởi động vì thay đổi kênh cập nhật add-on.
* Thêm khả năng bấm Control+Alt+mũi tên lên xuống để di chuyển giữa các
  track (riêng biệt, các cột của track) theo hàng dọc như là di chuyển đến
  dòng kế và dòng trước trong bảng.
* Thêm một hộp xổ trong hộp thoại cài đặt add-on để thiết lập cột nào được
  thông báo khi di chuyển qua chúng theo hàng dọc.
* Di chuyển các điều khiển cuối track , nhạc dạo và báo động microphone từ
  cài đặt add-on đến trung tâm báo động mới.
* Trong trung tâm báo động, trường nhập liệu cuối track và track giới thiệu
  đã luôn hiển thị có đánh dấu chọn vào hộp kiểm thông báo báo động hay
  không.
* Thêm lệnh trong SPL Assistant để thu thập các ảnh chụp danh sách phát như
  số track, track dài nhất, ca sĩ tiêu biểu và nhiều nữa (F8). Bạn cũng có
  thể thêm lệnh tùy chỉnh cho tính năng này.
* Bấm thao tác tùy chỉnh của lệnh chụp ảnh danh sách phát một lần sẽ cho
  phép NVDA đọc và hiện một thông tin ngắn về ảnh chụp trên màn hình
  nổi. Bấm hai lần để NVDA mở một trang web với đầy đủ thông tin hơn về ảnh
  chụp danh sách phát. Bấm escape để đóng trang web này.
* Gỡ bỏ lệnh Track Dial (phiên bản NVDA có cải tiến các phím mũi tên), thay
  thế bởi lệnh khám phá cột và điều hướng cột / lệnh điều hướng trong
  bảng). Điều này ảnh hưởng đến Studio và Trrack Tool.
* Sau khi đóng hộp thoại chèn track trong lúc đang thực hiện quét thư viện,
  không còn yêu cầu phải bấm SPL Assistant, Shift+R để theo dõi tiến trình
  quét.
* Cải thiện độ chính xác khi phát hiện và báo cáo việc hoàn thành quét thư
  viện trong Studio 5.10 trở lên. Điều này sửa một lỗi làm cho việc theo dõi
  quét thư viện bị ngưng sớm khi có nhiều track để quét, cần phải khởi động
  lại việc theo dõi quét thư viện.
* Cải thiện khả năng thông báo trạng thái quét thư viện thông qua bộ điều
  khiển SPL (Shift+R) bằng cách thông báo số lượng quét nếu có diễn ra quá
  trình này.
* Trong studio bản dùng thử (Demo), khi màn hình đăng kí xuất hiện lúc khởi
  động Studio, các lệnh như xem thời gian còn lại của track sẽ không còn
  tình trạng làm cho NVDA không làm gì, phát âm thanh báo lỗi hay cung cấp
  sai thông tin. Thay vào đó, thông điệp báo lỗi sẽ được thông báo. Các lệnh
  như vầy yêu cầu trình bày handle cửa sổ chính của Studio.
* Bắt đầu hỗ trợ cho StationPlaylist Creator.
* Thêm lệnh mới trong bộ điều khiển SPL để thông báo trạng thái Studio như
  phát track và thông tin trạng thái microphone (Q).

## Phiên bản 17.03

* NVDA sẽ không còn tình trạng không làm gì hoặc phát âm thanh báo lỗi khi
  chuyển đến một hồ sơ theo thời gian.
* Cập nhật các bản dịch.

## Phiên bản 17.01/15.5-LTS

Lưu ý: 17.01.1/15.5A-LTS thay thế 17.01 vì lí do thay đổi đường dẫn của các
tập tin add-on mới.

* 17.01.1/15.5A-LTS: thay đổi nơi tải các cập nhật cho các bản phát hành
  được hỗ trợ dài hạn. Cài đặt phiên bản này là bắt buộc.
* Cải thiện khả năng phản hồi và độ tin cạy khi dùng add-on để chuyển sang
  Studio, bất kể là dùng lệnh chuyển con trỏ về Studio từ một chương trình
  khác hay khi một bộ mã hóa được kết nối và NVDA được yêu cầu chuyển sang
  Studio. Nếu Studio đang được thu nhỏ, cửa sổ Studio sẽ hiển thị là không
  sẵn sàng. Trường hợp này, hãy phục hồi cửa sổ Studio từ khay hệ thống.
* Nếu chỉnh sửa cart khi Cart Explorer đang hoạt động, không còn cần thiết
  phải vào lại Cart Explorer để xem các cập nhật đã gán cho cart khi tắt chế
  độ chỉnh sửa cart. Kết quả là sẽ không còn thông báo yêu cầu vào lại Cart
  explorer..
* Trong add-on 15.5-LTS, chỉnh sửa giao diện người dùng cho hộp thoại cài
  đặt SPL add-on.

## Phiên bản 16.12.1

* Sửa giao diện người dùng của  hộp thoại cài đặt SPL add-on.
* Cập nhật các bản dịch.

## Phiên bản 16.12/15.4-LTS

* Hỗ trợ nhiều hơn cho Studio 5.20, bao gồm thông báo trạng thái chế độ chèn
  cart (nếu được bật) từ SPL Assistant layer (T).
* Bật tắt chế độ chỉnh sửa / chèn cart sẽ không còn bị ảnh hưởng bởi cấp độ
  đọc thông điệp và cài đặt kiểu thông báo trạng thái (trạng thái này sẽ
  luôn được thông báo qua bộ đọc và màn hình nổi).
* Không còn có thể thêm chú thích vào các lưu ý ngắt thời gian.
* Hỗ trợ cho Track Tool 5.20, bao gồm sửa một lỗi thông báo sai thông tin
  khi dùng lệnh khám phá cột để xem các thông tin cột.

## Phiên bản 16.11/15.3-LTS

* Bắt đầu hỗ trợ cho StationPlaylist Studio 5.20, bao gồm cải thiện khả năng
  phản hồi khi thu thập các thông tin trạng thái như tự động hóa thông qua
  SPL Assistant layer.
* Sửa lỗi liên quan đến tìm kiếm và tương tác với track, bao gồm việc không
  có khả năng chọn hay không chọn track đánh dấu hay một track tìm thấy
  thông qua hộp thoại tìm kiếm theo thời gian.
* Sắp xếp thông báo cột sẽ không còn bị trả về mặc định sau khi thay đổi nó.
* 16.11: nếu các hồ sơ phát thanh bị lỗi, hộp thoại báo lỗi sẽ không bị trục
  trặc và không hiển thị được.

## Phiên bản 16.10.1/15.2-LTS

* Giờ bạn có thể tương tác với track được tìm thấy qua tìm kiếm track
  (Control+NVDA+F) như là kiểm tra để phát lại.
* Cập nhật các bản dịch.

## Phiên bản 8.0/16.10/15.0-LTS

Phiên bản 8.0 (cũng được biết đến là 16.10) hỗ trợ SPL Studio 5.10 trở lên,
với 15.0-LTS (trước kia là 7.x) được thiết kế để cung cấp vài tính năng mới
từ 8.0 cho người dùng các phiên bản cũ của Studio. Cho đến khi có các ghi
chú khác, các mục dưới đây áp dụng cho cả 8.0 và 7.x. Một hộp thoại cảnh báo
sẽ hiển thị ở lần đầu sử dụng add-on 8.0 với Studio 5.0x được cài đặt, yêu
cầu bạn dùng phiên bản 15.x LTS.

* Kiểu tên phiên bản đã được thay đổi để thể hiện năm, tháng phát hành thay
  vì là phiên bản chính, phụ. Trong quá trình chuyển đổi (đến giữa năm
  2017), phiên bản 8.0 được xem như 16.10, với 7.x LTS đang được hiểu là
  15.0 vì các thay đổi không tương thích.
* Mã nguồn Add-on giờ đây được lưu trên GitHub (tại
  https://github.com/josephsl/stationPlaylist).
* Thêm hộp thoại chào mừng sẽ chạy khi khởi động Studio sau khi cài đặt
  add-on. Lệnh (Alt+NvDA+F1) đã được thêm vào để mở lại hộp thoại này.
* Thay đổi nhiều phím lệnh của add-on, bao gồm gỡ bỏ lệnh bật tắt thông báo
  trạng thái (Control+NvDA+1), sửa lệnh báo động cuối track thành
  Alt+NVDA+1, bật / tắt Cart Explorer là Alt+NvDA+3, hộp thoại báo động
  microphone là Alt+NVDA+4 và hộp thoại cài đặt add-on / bộ mã hóa là
  Alt+NvDA+0. Điều này cho phép gán Control+NVDA+phím số cho khám phá cột.
* 8.0: nới lỏng giới hạn khám phá cột như với phiên bản 7.x nên các phím 1
  đến 6 có thể cấu hình để thông báo cột trong Studio 5.1x.
* 8.0: lệnh bật / tắt Track Dial và các thiết lập tương ứng trong cài đặt
  add-on không còn dùng nữa và sẽ bị gỡ bỏ trong bản 9.0. Lệnh này vẫn còn
  trong add-on 7.x.
* Đã thêm Control+Alt+Home/End để chuyển con trỏ điều hướng đến cột đầu hay
  cuối trong trình xem danh sách phát.
* Giờ bạn có thể thêm, xem, thay đổi hoặc xóa các chú thích track. Bấm
  Alt+NVDA+C tại một track trong trình xem danh sách phát để nghe chú thích
  track nếu có, bấm hai lần để sao chép chú thích lên bộ nhớ tạm và ba lần
  để mở hộp thoại chỉnh sửa các chú thích.
* Thêm khả năng thông báo khi có chú thích track, và cũng thêm một thiết lập
  trong cài đặt add-on để điều khiển việc nó hoạt động như thế nào.
* Thêm một thiết lập trong hộp thoại  cài đặt add-on để NVDA thông báo nếu
  bạn đi về đầu hay cuối trình xem danh sách phát.
* Khi khôi phục các cài  đặt add-on, bạn có thể chỉ định phần nào sẽ được
  khôi phục. Mặc định, các thiết lập cho add-on sẽ được khôi phục, với các
  hộp kiểm cho việc khôi phục các hồ sơ chuyển nhanh, hồ sơ theo thời gian,
  thiết lập cho bộ mã hóa và xóa các chú thích track đã được thêm vào hộp
  thoại khôi phục cài đặt.
* Trong Track Tool, bạn có thể thu thập thông tin của album và mã CD bằng
  phím lệnh Control+NVDA+9 và Control+NVDA+0.
* Cải thiện sự vận hành khi lần đầu tiên thu thập thông tin cột trong Track
  Tool.
* 8.0: thêm một hộp thoại trong cài đặt add-on để cấu hình việc khám phá cột
  cho Track Tool.
* Giờ bạn có thể cấu hình thời gian báo động microphone từ hộp thoại báo
  động microphone (Alt+NvDA+4).

## Phiên bản 7.5/16.09

* NVDA sẽ không còn hiện hộp thoại tiến trình cập nhật nếu vừa thay đổi kênh
  cập nhật add-on.
* NVDA sẽ thông báo kênh cập nhật đã chọn khi đang tải cập nhật.
* Cập nhật các bản dịch.

## Phiên bản 7.4/16.08

Phiên bản 7.4 cũng được biết đến là 16.08 căn cứ vào số phiên bản phát hành
chính thức theo năm.tháng.

* Việc có thể chọn kênh cập nhật add-on từ cài đặt add-on /tùy chọn nâng
  cao, sẽ bị gỡ bỏ trong năm 2017. Với 7.4, các kênh bao gồm beta, stable và
  long-term.
* Đã thêm một thiết lập trong  cài đặt add-on/tùy chọn nâng cao để cấu hình
  thời gian kiểm tra cập nhật trong khoảng 1 đến 30 ngày (mặc định là 7 hoặc
  kiểm tra mỗi tuần).
* Lệnh của bộ điều khiển SPL và lệnh đưa con trỏ về Studio sẽ không hoạt
  động ở màn hình bảo vệ.
* Cập nhật và thêm vào các bản dịch cho nhiều ngôn ngữ.

## Các thay đổi cho phiên bản 7.3

* Cải thiện hiệu suất nhẹ khi tìm kiếm các thông tin như tự động hóa thông
  qua vài lệnh SPL Assistant.
* Cập nhật các bản dịch.

## Các thay đổi cho phiên bản 7.2

* Do việc gỡ bỏ kiểu cấu hình định dạng nội bộ cũ, bắt buộc phải cài đặt
  add-on 7.2. Khi đã cài rồi, bạn không thể trở về một phiên bản cũ hơn của
  add-on.
* Thêm lệnh trong bộ điều khiển SPL để thông báo lượng người nghe (I).
* Giờ bạn có thể mở các hộp thoại cài đặt SPL add-on và cài đặt bộ mã hóa
  bằng cách bấm Alt+NVDA+0. Bạn vẫn có thể dùng Control+NVDA+0 để mở chúng
  (sẽ bị gỡ bỏ trong add-on 8.0).
* Trong Track Tool, bạn có thể dùng Control+Alt+mũi tên trái phải để điều
  hướng giữa các cột.
* Nội dung của nhiều hộp thoại khác nhau trong Studio như hộp thoại About
  trong Studio 5.1x giờ đây đã được thông báo.
* Trong các bộ mã hóa SPL, NVDA sẽ không phát âm thanh kết nối nếu bật tùy
  chọn tự kết nối rồi tắt từ trình đơn ngữ cảnh của bộ mã hóa khi nó đang
  được kết nối.
* Cập nhật các bản dịch.

## Các thay đổi cho phiên bản 7.1

* Sửa các lỗi gặp phải  khi nâng cấp từ add-on 5.5 hay thấp hơn lên 7.0.
* Trả lời "không" khi khôi phục các cài đặt add-on, bạn sẽ được đưa về hộp
  thoại cài đặt add-on và NVDA sẽ nhớ thiết lập cho hồ sơ chuyển nhanh.
* NVDA sẽ yêu cầu bạn cấu hình lại các nhãn phát thanh và các tùy chọn mã
  hóa khác nếu tập tin cấu hình mã hóa bị hư hỏng.

## Các thay đổi cho phiên bản 7.0

* Thêm tính năng kiểm tra cập nhật add-on. Tính năng này có thể thực hiện
  thủ công (SPL Assistant, Control+Shift+U) hoặc tự động (được cấu hình
  thông qua hộp thoại tùy chọn nâng cao từ cài đặt add-on).
* Không còn yêu cầu phải đứng trong cửa sổ trình xem danh sách phát để gọi
  hầu hết các lệnh của SPL Assistant layer hoặc thu thập các thông báo về
  thời gian như thời gian còn lại của track và thời gian phát thanh.
* Các thay đổi cho lệnh SPL Assistant, bao gồm thời lượng danh sách phát
  (D), đổi lệnh chọn thời lượng theo giờ từ Shift+H thành Shift+S và Shift+H
  giờ đây dùng để thông báo thời lượng của các track còn lại trong khung giờ
  hiện tại, lệnh trạng thái metadata streaming được gán lại (1 đến 4, 0 đổi
  thành Shift+1 đến Shift+4, Shift+0).
* Giờ đây đã có thể gọi lệnh tìm kiếm track thông qua SPL Assistant (F).
* SPL Assistant, các số từ 1 đến 0 (6 với Studio 5.01 trở xuống) có thể dùng
  để thông báo các thông tin cột. Các cột này có thể thay đổi trong mục khám
  phá cột trong hộp thoại cài đặt add-on.
* Sửa nhiều lỗi  do người dùng báo về khi lần đầu cài đặt add-on 7.0 mà
  không có phiên bản thấp hơn được cài trước đó.
* Các cải thiện cho Track Dial, bao gồm cải thiện khả năng phản hồi khi di
  chuyển qua các cột và theo dõi việc các cột được trình bày trên màn hình
  như thế nào.
* Thêm tính năng bấm Control+Alt+mũi tên trái phải để di chuyển giữa các cột
  của track.
* Giờ đây, đã có thể dùng các kiểu phím tắt của các trình đọc màn hình khác
  nhau cho lệnh SPL Assistant. Vào hộp thoại tùy chọn nâng cao từ cài đặt
  add-on để cấu hình tùy chọn này giữa NVDA, JAWS và Window-Eyes. Xem các
  lệnh SPL Assistant ở trên để biết thêm chi tiết.
* Có thể cấu hình để NVDA chuyển sang một hồ sơ phát thanh cụ thể ở một thời
  điểm cụ thể. Dùng hộp thoại tác nhân mới trong cài đặt add-on để thực hiện
  điều này.
* NVDA sẽ thông báo tên của hồ sơ khi nó được chuyển sang thông qua hồ sơ
  chuyển nhanh (SPL Assistant, F12) hoặc một hồ sơ theo thời gian được kích
  hoạt.
* Chuyển tùy chọn bật / tắt hồ sơ chuyển nhanh (giờ đây là một hộp kiểm) đến
  hộp thoại tác nhân mới.
* Các thành phần của hộp xổ hồ sơ trong hộp thoại cài đặt add-on giờ đây
  hiển thị các thông tin hồ sơ như đang hoạt động, là hồ sơ chuyển nhanh và
  nhiều nữa.
* Nếu một vấn đề nghiêm trọng trong việc đọc các tập tin hồ sơ phát thanh
  được tìm thấy, NVDA sẽ hiển thị hộp thoại báo lỗi và khôi phục các cài đặt
  về mặc định thay vì phát âm thanh báo lỗi hay không làm gì.
* Các thiết lập sẽ được lưu xuống đĩa khi và chỉ khi bạn thay đổi
  chúng. Điều này sẽ kéo dài tuổi thọ của đĩa SSD (ổ đĩa trạng thái rắn)
  bằng cách ngăn chặn việc lưu xuống đĩa ngoài ý muốn khi không có thay đổi
  thiết lập nào được thực hiện.
* Trong hộp thoại cài đặt add-on, các điều khiển để bật / tắt các thông báo
  thời gian đã lên lịch, số lượng người nghe, tên cart và tên track đã được
  chuyển đến một hộp thoại thông báo trạng thái riêng (chọn nút thông báo
  trạng thái để mở hộp thoại này).
* Thêm một thiết lập mới trong hộp thoại cài đặt add-on để NVDA phát tiếng
  beep cho các loại track khác nhau khi di chuyển giữa các track trong trình
  xem danh sách phát.
* Việc cố gắng mở tùy chọn cấu hình metadata trong hộp thoại cài đặt add-on
  khi hộp thoại quick metadata streaming đang mở sẽ không còn khiến NVDA
  phát âm thanh báo lỗi hoặc không làm gì. Giờ đây, NvDA sẽ yêu cầu bạn đóng
  hộp thoại metadata streaming trước khi mở cài đặt add-on.
* Khi thông báo thời gian còn lại cho track đang phát chẳng hạn, giờ cũng
  được thông báo. Kết quả, thiết lập thông báo giờ mặc định được bật.
* Bấm điều khiển SPL, giờ đây sẽ khiến cho NVDA thông báo thời gian còn lại
  theo định dạng giờ, phút và giây (phút và giây nếu là trường hợp như vậy).
* Trong các bộ mã hóa, bấm Control+NVDA+0 sẽ hiện hộp thoại cài đặt mã hóa
  để cấu hình nhiều tùy chọn như nhãn phát thanh, đưa con trỏ về cửa sổ
  Studio khi kết nối và nhiều nữa.
* Trong các bộ mã hóa, giờ đây đã có thể tắt âm báo tiến trình kết nối (cấu
  hình từ hộp thoại cài đặt mã hóa).

## Các thay đổi cho phiên bản 6.4

* Sửa một lỗi khi chuyển về từ một hồ sơ chuyển nhanh và hồ sơ chuyển nhanh
  hoạt động trở lại, được thấy sau khi xóa một hồ sơ đã hoạt động trước
  đó. Khi cố gắng xóa một hồ sơ, một hộp thoại cảnh báo sẽ hiện ra nếu có
  một hồ sơ chuyển nhanh hoạt động.

## Các thay đổi cho phiên bản 6.3

* Các cải tiến bảo mật bên trong.
* Khi add-on 6.3 trở lên được gọi chạy lần đầu trên một máy tính cài đặt
  Windows 8 trở lên với NVDA 2016.1 trở lên, một hộp thoại cảnh báo sẽ hiển
  thị yêu cầu bạn tắt chế độ giảm âm (NVDA+Shift+D). Chọn vào hộp kiểm để
  không hiện hộp thoại này nữa.
* Thêm lệnh để gửi báo lỗi, gợi ý tính năng và các phản hồi khác cho nhóm
  phát triển add-on (Control+NVDA+trừ (-)).
* Cập nhật các bản dịch.

## Các thay đổi cho phiên bản 6.2

* Sửa một lỗi với lệnh xem phần còn lại của danh sách phát (SPL Assistant, D
  (R nếu chế độ tương thích được bật)) khi thời lượng của khung giờ hiện tại
  được thông báo đối lập với toàn bộ danh sách phát (hoạt động của lệnh này
  có thể cấu hình từ cài đặt nâng cao tìm thấy trong hộp thoại cài đặt
  add-on).
* Giờ đây, NvDA có thể thông báo tên của track đang phát khi dùng các chương
  trình khác (cấu hình từ cài đặt add-on).
* Thiết lập được dùng để bộ điều khiển SPL gọi SPL Assistant giờ đây được
  tôn trọng (trước đó nó được bật mọi lúc).
* Trong SAM encoders, các lệnh Control+F9 và Control+F10 giờ đã làm việc
  chính xác.
* Trong các bộ mã hóa, khi con  trỏ đứng tại bộ mã hóa đầu tiên và nếu nó
  được cấu hình để theo dõi ngầm, NVDA giờ đây sẽ tự động ngầm theo dõi.

## Các thay đổi cho phiên bản 6.1

* Thông báo việc sắp xếp và bao gồm các cột, kể cả thiết lập của metadata
  streaming giờ đây sẽ là hồ sơ thiết lập cụ thể.
* Khi thay đổi các hồ sơ, sẽ bật chính xác metadata stream.
* Khi mở hộp thoại cài đặt quick metadata streaming (chưa gán lệnh), những
  thiết lập được thay đổi sẽ áp dụng cho hồ sơ đang hoạt động.
* Khi khởi động Studio, thay đổi cách hiển thị lỗi nếu hồ sơ bị lỗi chỉ là
  hồ sơ bình thường.
* Khi thay đổi một số thiết lập nhất định bằng phím tắt như thông báo trạng
  thái, sửa một lỗi làm cho các thiết lập đã thay đổi không được lưu lại khi
  chuyển đến hay chuyển đi khỏi một hồ sơ chuyển nhanh.
* Khi dùng một lệnh SPL Assistant với một thao tác tùy chỉnh  (như là track
  kế), không còn bắt buộc phải đứng trong trình xem danh sách phát của
  Studio mới dùng được các lệnh này (chúng có thể được thực hiện ở các cửa
  sổ Studio khác).

## Các thay đổi cho phiên bản 6.0

* Các lệnh mới cho SPL Assistant, bao gồm thông báo tựa đề của track đang
  phát (C), thông báo trạng thái metadata streaming (E, 1 đến 4 và 0) và mở
  tài liệu hướng dẫn trực tuyến (Shift+F1).
* Khả năng đóng gói các thiết lập ưa thích như hồ sơ phát thanh để dùng
  trong một chương trình biểu diễn và chuyển đến một hồ sơ đã được chỉ
  định. Xem hướng dẫn sử dụng add-on để biết các chi tiết về hồ sơ phát
  thanh.
* Đã thêm một thiết lập mới trong cài đặt add-on để điều khiển cấp độ đọc
  thông điệp (vài thông điệp sẽ được rút ngắn khi cấp độ nâng cao được
  chọn).
* Thêm một thiết lập mới trong cài đặt add-on để NVDA thông báo giờ, phút và
  giây cho track hay thời lượng danh sách phát (các tính năng chịu ảnh hưởng
  bao gồm thông báo thời gian đã qua hay còn lại của track đang phát, phân
  tích thời gian track và nhiều nữa).
* Giờ bạn có thể yêu cầu NVDA thông báo tổng độ dài cho một vùng các track
  thông qua tính năng phân tích thời gian track. Bấm SPL Assistant, F9 để
  đánh dấu track hiện tại là điểm bắt đầu, chuyển đến track cuối của vùng và
  bấm SPL Assistant, F10. Các lệnh này có thể gán lại nên không cần phải gọi
  SPL Assistant layer để thực hiện phân tích thời gian track.
* Thêm hộp thoại tìm kiếm cột (chưa gán thao tác) để tìm kiếm nội dung trong
  các cột cụ thể như tên ca sĩ hay một phần tên tập tin.
* Thêm hộp thoại tìm kiếm khoảng thời gian (chưa gán thao tác) để tìm một
  track với thời lượng nằm trong khoảng thời gian được chỉ định, hữu dụng
  nếu muốn tìm một track để lấp đầy một khung giờ.
* Thêm khả năng sắp xếp lại việc thông báo cột của track và tắt thông báo
  của một số cột nhất định nếu bỏ chọn "dùng sắp xếp theo màn hình" từ hộp
  thoại cài đặt add-on. Dùng hộp thoại "quản lý thông báo cột" để ắp xếp
  lại.
* Đã thêm một hộp thoại (chưa gán thao tác) để bật / tắt nhanh metadata
  streaming.
* Thêm một thiết lập trong hộp thoại cài đặt add-on để cấu hình khi nào thì
  thông báo trạng thái metadata streaming và để bật metadata streaming.
* Thêm khả năng dùng một track làm điểm đánh dấu để trở lại sau đó (SPL
  Assistant, Control+K để gán, SPL Assistant, K để chuyển đến track đã đánh
  dấu).
* Cải thiện khả năng vận hành khi  tìm kiếm track kế hay track trước đã có
  nội dung tìm kiếm.
* Thêm một thiết lập trong hộp thoại cài đặt add-on để cấu hình thông báo
  báo động (beep, thông điệp hoặc cả hai).
* Giờ đã có thể cấu hình báo động microphone trong khoảng 0 (tắt) và 2 giờ
  (7200 giây) và dùng mũi tên lên xuống để cấu hình.
* Thêm một thiết lập trong hộp thoại cài đặt add-on cho phép việc microphone
  hoạt động được thông báo định kì.
* Giờ bạn có thể dùng lệnh  bật / tắt Track Dial trong Studio để bật / tắt
  Track Dial trong Track Tool được cung cấp khi bạn không gán lệnh để bật /
  tắt Track Dial trong Track Tool.
* Thêm khả năng dùng lệnh SPL Controller layer để gọi SPL Assistant layer
  (cấu hình từ hộp thoại cài đặt nâng cao tìm thấy trong hộp thoại cài đặt
  add-on).
* Thêm khả năng để NvDA dùng một số lệnh SPL Assistant nhất định được dùng
  bởi các trình đọc màn hình khác. Để cấu hình, mở cài đặt add-on, chọn cài
  đặt nâng cao và chọn hộp kiểm chế độ tương thích trình đọc màn hình.
* Trong các bộ mã hóa, các thiết lập như đứng tại Studio khi kết nối đã được
  ghi nhớ.
* Giờ đã có thể xem nhiều cột khác nhau từ cửa sổ mã hóa (như trạng thái kết
  nối bộ mã hóa) thông qua Control+NVDA+các phím số; xem các lệnh mã hóa ở
  trên.
* Sửa một lỗi hiếm gặp khi chuyển đến Studio hay đóng một hộp thoại của NVDA
  (bao gồm các hộp thoại của Studio add-on) làm các lệnh của track (như là
  bật / tắt Track Dial) không hoạt động như ý muốn.

## Các thay đổi cho phiên bản 5.6

* Trong Studio 5.10 trở lên, NVDA không còn thông báo "chưa chọn" khi đang
  phát track đã chọn.
* Vì một vấn đề với Studio, NVDA giờ đây sẽ tự thông báo tên của track đang
  phát. tùy chọn để bật / tắt nó đã được thêm vào hộp thoại cài đặt add-on
  cho studio.

## Các thay đổi cho phiên bản 5.5

* Thiết lập phát sau khi kết nối sẽ được ghi nhớ khi chuyển khỏi cửa sổ mã
  hóa.

## Các thay đổi cho phiên bản 5.4

* Thực hiện quét thư viện từ hộp thoại chèn track không còn làm cho NVDA
  không thông báo trạng thái quét hay phát âm thanh báo lỗi nếu NVDA được
  cấu hình để thông báo tiến trình quét thư viện hay lượt quét.
* Cập nhật các bản dịch.

## Các thay đổi cho phiên bản 5.3

* Sửa lỗi cho  SAM Encoder (không phát track kế nếu đang phát một track và
  khi kết nối một bộ mã hóa) giờ đây đã có tác dụng cho người dùng bộ mã hóa
  SPL.
* NVDA không còn phát âm thanh báo lỗi hoặc không làm gì khi bấm SPL
  Assistant, F1 hộp thoại (trợ giúp Assistant).

## Các thay đổi cho phiên bản 5.2

* NVDA sẽ không còn cho phép cả hộp thoại cài đặt và báo động mở cùng
  lúc. Một cảnh báo sẽ hiển thị yêu cầu bạn đóng hộp thoại đã mở trước đó
  rồi mới mở một hộp thoại khác.
* Khi theo dõi một hay nhiều bộ mã hóa, bấm SPL Controller, E giờ đây sẽ
  thông báo số lượng bộ mã hóa, ID bộ mã hóa và nhãn phát thanh nếu có.
* NVDA hỗ trợ kết nối / ngắt kết nối tất cả lệnh (Control+F9/Control+F10)
  trong SAM encoders.
* NVDA sẽ không còn phát track kế nếu kết nối một bộ mã trong khi Studio
  đang phát một track và được thiết lập phát track khi một bộ mã hóa được
  kết nối.
* Cập nhật các bản dịch.

## Các thay đổi cho phiên bản 5.1

* Giờ đã có thể xem các cột cụ thể trong Track Tool thông qua Track Dial
  (phím bật / tắt chưa được gán). Lưu ý rằng Studio phải được kích hoạt
  trước khi dùng chế độ này.
* Thêm một hộp kiểm trong hộp thoại cài đặt Studio add-on để bật / tắt thông
  báo tên của cart đang phát.
* Bật / tắt microphone thông qua bộ điều khiển SPL không còn phát âm thanh
  báo lỗi hay tắt âm báo.
* Nếu gán một lệnh tùy chỉnh cho lệnh SPL Assistant layer và lệnh này được
  bấm ngay sau khi vào SPL Assistant, NvDA sẽ thoát SPL Assistant một cách
  kịp thời.

## Các thay đổi cho phiên bản 5.0

* Một hộp thoại cài đặt chuyên dụng cho SPL add-on đã được thêm, tiếp cận từ
  trình đơn tùy  chỉnh của NVDA hoặc bấm Control+NVDA+0 từ cửa sổ SPL.
* Thêm khả năng khôi phục tất cả các cài đặt về mặc định thông qua hộp thoại
  cấu hình.
* Nếu có lỗi từ vài thiết lập, chỉ các thiết lập bị ảnh hưởng sẽ khôi phục
  về thiết lập của nhà phát triển.
* Thêm chế độ và thao tác cảm ứng chuyên dụng cho SPL để thực hiện nhiều
  lệnh khác nhau của Studio.
* Các thay đổi cho SPL Assistant layer bao gồm thêm lệnh trợ giúp (F1) và gỡ
  bỏ lệnh bật / tắt số lượng người nghe (Shift+I) và thông báo thời gian đã
  lên lịch (Shift+S). Bạn có thể cấu hình các thiết lập này trong hộp thoại
  cài đặt add-on.
* Đổi tên "bật / tắt thông báo" thành "thông báo trạng thái" vì tiếng beep
  đã dùng để thông báo các thông tin trạng thái khác như hoàn thành việc
  quét thư viện.
* Thiết lập thông báo trạng thái giờ đây được giữ lại qua các phiên làm
  việc. Trước đây bạn phải cấu hình thủ công thiết lập này khi khởi động
  Studio.
* Giờ bạn có thể dùng tính năng Track Dial để xem các cột trong một track
  trong trình xem danh sách phát chính của Studio (để bật / tắt tính năng
  này, bấm lệnh mà bạn đã gán cho nó).
* Giờ bạn có thể gán các lệnh tùy chỉnh để nghe thông tin về nhiệt độ hay
  thông báo tựa đề của track sắp tới nếu được lên lịch.
* Thêm một hộp kiểm trong các hộp thoại báo động nhạc dạo và cuối track để
  bật / tắt các báo động này (chọn để bật). These can also be "configured"
  from add-on settings.
* Sửa lỗi khi bấm lệnh mở các hộp thoại báo động hay tìm kiếm track khi một
  hộp thoại báo động hay tìm kiếm track khác đang mở làm xuất hiện một hộp
  thoại cùng loại. NVDA sẽ hiện một thông điệp yêu cầu bạn đóng các hộp
  thoại đã mở trước đó.
* Cart explorer đã sửa và thay đổi, bao gồm xem sai ngân hàng cart  khi
  người dùng không đứng tại trình xem danh sách phát. Cart explorer giờ đây
  sẽ kiểm tra để chắc rằng bạn đang trong trình xem danh sách phát.
* Thêm khả năng dùng lệnh SPL Controller layer để gọi SPL Assistant (thử
  nghiệm; xem hướng dẫn sử dụng add-on để biết làm thế nào để bật tính năng
  này).
* Trong cửa sổ mã hóa, lệnh thông báo ngày giờ của NVDA (mặc định là
  NVDA+F12) sẽ thông báo giờ bao gồm cả giây.
* Giờ bạn có thể theo dõi các bộ mã hóa riêng biệt cho các trạng thái kết
  nối và các thông điệp khác bằng cách bấm Control+F11 khi bộ mã hóa bạn
  muốn theo dõi đang tại vị trí con trỏ (làm việc tốt hơn khi dùng SAM
  encoders).
* Đã thêm lệnh trong bộ điều khiển SPL để thông báo trạng thái của các bộ mã
  hóa đang được theo dõi (E).
* Giờ đây, đã có cách giải quyết cho lỗi làm NvDA thông báo nhãn phát thanh
  cho các bộ mã hóa sai, đặc biệt là sau khi xóa một bộ mã hóa (để sắp xếp
  lại nhãn phát thanh, bấm Control+F12, rồi chọn vị trí của bộ mã hóa bạn đã
  gỡ bỏ).

## Các bản phát hành cũ hơn

Vui lòng xem liên kết bản ghi các thay đổi để có thông tin về các bản phát
hành cũ của add-on.

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=spl

[2]: https://addons.nvda-project.org/files/get.php?file=spl-dev

[3]: https://addons.nvda-project.org/files/get.php?file=spl-lts18

[4]: https://github.com/josephsl/stationplaylist/wiki/SPLAddonGuide

[5]: https://github.com/josephsl/stationplaylist/wiki/splchangelog
