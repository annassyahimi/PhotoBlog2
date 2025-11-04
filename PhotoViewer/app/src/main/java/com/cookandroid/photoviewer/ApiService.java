package com.cookandroid.photoviewer;

import java.util.List;

import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface ApiService {

    @Multipart
    @POST("upload/")
    Call<ResponseBody> uploadPhoto(
            @Part MultipartBody.Part image,
            @Part("title") RequestBody title
    );

    @GET("photos/")
    Call<List<PhotoItem>> getPhotos();
}
