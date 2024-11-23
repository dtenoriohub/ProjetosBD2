package org.example.entity;

import javax.persistence.*;

@Entity
@Table(name = "cabras")
public class Cabra {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String raca;

    @Column(nullable = false)
    private Integer idade;

    @Column(nullable = false, unique = true)
    private String numeroIdentificacao;

    // Getters e Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getRaca() {
        return raca;
    }

    public void setRaca(String raca) {
        this.raca = raca;
    }

    public Integer getIdade() {
        return idade;
    }

    public void setIdade(Integer idade) {
        this.idade = idade;
    }

    public String getNumeroIdentificacao() {
        return numeroIdentificacao;
    }

    public void setNumeroIdentificacao(String numeroIdentificacao) {
        this.numeroIdentificacao = numeroIdentificacao;
    }
}
