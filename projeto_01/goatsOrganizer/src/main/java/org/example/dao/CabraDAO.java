package org.example.dao;

import org.example.entity.Cabra;
import org.example.util.HibernateUtil;
import org.hibernate.Session;
import org.hibernate.Transaction;
import java.util.List;

public class CabraDAO {
    public void salvar(Cabra cabra) {
        Transaction transaction = null;
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            transaction = session.beginTransaction();
            session.save(cabra);
            transaction.commit();
        } catch (Exception e) {
            if (transaction != null) transaction.rollback();
            e.printStackTrace();
        }
    }

    public void atualizar(Cabra cabra) {
        Transaction transaction = null;
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            transaction = session.beginTransaction();
            session.update(cabra);
            transaction.commit();
        } catch (Exception e) {
            if (transaction != null) transaction.rollback();
            e.printStackTrace();
        }
    }

    public void deletar(Long id) {
        Transaction transaction = null;
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            transaction = session.beginTransaction();
            Cabra cabra = session.get(Cabra.class, id);
            if (cabra != null) {
                session.delete(cabra);
                transaction.commit();
            }
        } catch (Exception e) {
            if (transaction != null) transaction.rollback();
            e.printStackTrace();
        }
    }

    public Cabra buscarPorId(Long id) {
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            return session.get(Cabra.class, id);
        }
    }

    public List<Cabra> listarTodas() {
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            return session.createQuery("from Cabra", Cabra.class).list();
        }
    }
}
