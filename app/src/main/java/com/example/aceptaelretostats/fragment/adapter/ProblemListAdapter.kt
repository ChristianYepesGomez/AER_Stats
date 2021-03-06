package com.example.aceptaelretostats.fragment.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.aceptaelretostats.R
import com.example.aceptaelretostats.model.Problems


class ProblemListAdapter(private var problems: MutableList<Problems>) :
    RecyclerView.Adapter<ProblemListAdapter.MyViewHolder>() {


    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MyViewHolder {
        problems.sortByDescending { it.accepteds.toInt() }
        val itemView = LayoutInflater.from(parent.context).inflate(
            R.layout.list_problems,
            parent, false
        )
        return MyViewHolder(itemView)
    }

    override fun onBindViewHolder(holder: MyViewHolder, position: Int) {
        val currentItem = problems[position]
        holder.campoAccepteds.text = "Total AC: ".plus(currentItem.accepteds)
        holder.campoId.text = "Nº: ".plus(currentItem.id)
        holder.campoNombreProblema.text = currentItem.name
    }

    override fun getItemCount(): Int {
        return problems.size
    }

    class MyViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {

        val campoNombreProblema: TextView = itemView.findViewById(R.id.id_name_problem)
        val campoId: TextView = itemView.findViewById(R.id.id_problem)
        val campoAccepteds: TextView = itemView.findViewById(R.id.id_accepteds_problem)
    }

}