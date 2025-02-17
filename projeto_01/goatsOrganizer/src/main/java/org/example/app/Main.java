package org.example.app;


import org.example.dao.CabraDAO;
import org.example.entity.Cabra;

import java.util.List;

public class Main {
    public static void main(String[] args) {
        CabraDAO cabraDAO = new CabraDAO();

        /* Criar uma nova cabra
        Cabra cabra1 = new Cabra();
        cabra1.setRaca("Anglo Nubiana");
        cabra1.setIdade(8);
        cabra1.setNumeroIdentificacao("1234");
        cabraDAO.salvar(cabra1);*/

        // Deletar uma cabra
        cabraDAO.deletar(8L);
        //Listar todas as cabras


        /*listar cabras
        List<Cabra> cabras = cabraDAO.listarTodas();
        cabras.forEach(c -> System.out.println("ID: " + c.getId() + ", Raça: " + c.getRaca()));
*/

        /*
        // Atualizar uma cabra
        Cabra cabraAtualizada = cabraDAO.buscarPorId(8L);
        cabraAtualizada.setIdade(4);
        cabraAtualizada.setRaca("Saanen");
        cabraDAO.atualizar(cabraAtualizada);

        */
    }
}
