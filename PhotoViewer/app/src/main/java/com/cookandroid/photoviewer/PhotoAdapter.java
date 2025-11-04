package com.cookandroid.photoviewer;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import androidx.recyclerview.widget.RecyclerView;
import com.bumptech.glide.Glide;
import java.util.List;

public class PhotoAdapter extends RecyclerView.Adapter<PhotoAdapter.ViewHolder> {

    private List<PhotoItem> photoList;
    private Context context;

    public PhotoAdapter(Context context, List<PhotoItem> photoList) {
        this.context = context;
        this.photoList = photoList;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.item_photo, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {
        PhotoItem photo = photoList.get(position);
        holder.titleView.setText(photo.getTitle());
        Glide.with(context)
                .load(photo.getImage())  // Django full image URL
                .placeholder(android.R.drawable.ic_menu_gallery)
                .into(holder.imageView);
    }

    @Override
    public int getItemCount() {
        return photoList.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        ImageView imageView;
        TextView titleView;

        public ViewHolder(View itemView) {
            super(itemView);
            imageView = itemView.findViewById(R.id.imageView);
            titleView = itemView.findViewById(R.id.titleView);
        }
    }
}
