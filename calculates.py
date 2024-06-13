import adsk.core, adsk.fusion, adsk.cam, traceback

app = adsk.core.Application.get()
ui = app.userInterface
        
# def checkIfGrooving(component, face):
#     try:
#         # Yüzeyin komşu yüzeylerini al
#         neighborFaces = face.neighbors

#         # Her bir komşu yüzey için kontrol yap
#         for neighborFace in neighborFaces:
#             # Komşu yüzeyin normal vektörü
#             neighborNormal = neighborFace.geometry.normal

#             # Eğer komşu yüzey normali, yüzey normaline paralel ise
#             # bu durumda yüzeyler arasında bir oluk bulunuyor olabilir
#             if neighborNormal.isParallelTo(face.geometry.normal):
#                 # Başlangıç ve bitiş edge'leri bul
#                 startEdge = None
#                 endEdge = None
#                 # Yüzeyin tüm kenarlarını al
#                 edges = face.edges
#                 for edge in edges:
#                     # Eğer kenarın iki ucu da yüzeye ait değilse,
#                     # bu kenar oluğun başlangıç veya bitiş kenarı olabilir
#                     if not edge.startVertex.isVertexOnFace(face) or not edge.endVertex.isVertexOnFace(face):
#                         if startEdge is None:
#                             startEdge = edge
#                         else:
#                             endEdge = edge
#                             break
                
#                 # Başlangıç ve bitiş edge'leri bulunduysa, bunları döndür
#                 if startEdge and endEdge:
#                     return startEdge, endEdge

#         # Eğer oluk bulunamadıysa None döndür
#         return None, None
#     except:
#         # Hata durumunda hata mesajını yazdır
#         traceback.print_exc()
#         return None, None
        
def showMessage(message):
    app.log(message)

    # Give control back to Fusion, so it can update the UI.
    adsk.doEvents()