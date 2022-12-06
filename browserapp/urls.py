from django.urls import path
from . import views

app_name = "browse" # namespace used for reverse searching

urlpatterns = [
    #browse/
    path('', views.index_view, name = 'browse_index'),

    #browse/id
    path('<int:gid>', views.detail_view, name = 'browse_detail'),

    #browse/upload
    path('upload', views.create_view, name = 'browse_upload'),

    #browse/edit/id
    path('edit/<int:gid>', views.update_view, name = 'browse_edit'),

    #browse/delete/id
    path('delete/<int:gid>', views.delete_view, name = 'browse_delete'),


    #browse/publishers
    path('publishers', views.pubIndex_view, name = 'publisher_index'),

    #browse/publishers/upload
    path('publishers/upload', views.pubCreate_view, name = 'publisher_upload'),

    #browse/publishers/id
    path('publishers/<int:pid>', views.pubDetail_view, name = 'publisher_detail'),

    #browse/publishers/edit/id
    path('publishers/edit/<int:pid>', views.pubEdit_view, name = 'publisher_edit'),

    #browse/publishers/delete/id
    path('publishers/delete/<int:pid>', views.pubDelete_view, name = 'publisher_delete'),

    #browse/toggleGame
    #path('toggleGame', views.toggleGameView.as_view(), name = 'toggleGame'), # Unused add to library function, replaced by new AJAX


    #browse/myGames
    path('myGames', views.myGamesIndex, name = 'myGamesIndex'),

    # testing url for adding games
    #path('add/<int:gid>', views.addGametoLibrary, name = 'addGametoLibrary'),

    path('add', views.addGametoLibrary, name = 'addGametoLibrary'),
    
    
]

